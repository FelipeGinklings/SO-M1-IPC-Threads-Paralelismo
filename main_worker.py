#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import threading
import numpy as np
from constants import ImageMetadata, Header, PIPE_PATH, NEG_MODE, SLICE_MODE
import json
import multiprocessing
from concurrent.futures import ThreadPoolExecutor


# In[ ]:


def start_pipe_reader():
    print("Reader process started. Waiting for data...")

    # Open the pipe for reading (blocks until writer opens)
    payload = {}
    data = b""
    with open(PIPE_PATH, "rb") as pipe:
        while True:
            try:
                metadata = pipe.readline()
                if not metadata:
                    # Pipe was closed by writer
                    break
                payload = json.loads(metadata.decode())
                data = pipe.read(
                    payload["width"] * payload["height"]
                )
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    metadata = ImageMetadata(payload["height"], payload["width"], payload["maxv"], data)
    header = Header(payload['header']['mode'], payload['header']['slice_range'], payload['header']['colored'])
    return metadata, header


# In[ ]:


def image_negative_worker(start, end,result_lock, new_image, image):
    """Generate a negative for the image chunk of the image"""
    image_chunk = image[start:end].copy()
    new_image_chunk = 255 - image_chunk
    # Need lock when updating shared result
    with result_lock:
        new_image[start:end] += new_image_chunk

def threshold_with_slicing_worker(start, end,result_lock, new_image, image, limits, maxv):
    """Generate a negative for the image chunk of the image"""
    a, b = limits
    image_chunk = image[start:end].copy()
    mask = (image_chunk > a) & (image_chunk < b)
    new_image_chunk = np.where(mask, maxv, image_chunk)

    # Need lock when updating shared result
    with result_lock:
        new_image[start:end] = new_image_chunk


# In[ ]:


def calculate_image_threads(height, min_rows_per_thread=50, max_threads=16):
    """
    Calculate threads for image processing

    Args:
        height: Image height in pixels
        min_rows_per_thread: Minimum rows to avoid overhead
        max_threads: Upper limit
    """
    cpu_cores = multiprocessing.cpu_count()

    # Maximum threads possible based on rows
    max_threads_by_rows = max(1, height // min_rows_per_thread)

    # Optimal threads (can't have more threads than rows)
    optimal = min(cpu_cores, max_threads_by_rows, max_threads)

    # Keep at least one CPU core free when all cores would be used
    if optimal == cpu_cores and optimal > 1:
        optimal -= 1

    # Ensure each thread gets reasonable work
    if optimal > 1:
        rows_per_thread = height // optimal
        if rows_per_thread < min_rows_per_thread:
            optimal = max(1, height // min_rows_per_thread)
            if optimal == cpu_cores and optimal > 1:
                optimal -= 1

    return optimal


# In[ ]:


def get_image_slice_values(metadata, colored=False):
    threads = calculate_image_threads(metadata.height)

    width, height = metadata.width, metadata.height
    if colored:
        image = np.frombuffer(metadata.data, dtype=np.uint8).reshape(height, width, 3)
    else:
        image = np.frombuffer(metadata.data, dtype=np.uint8).reshape(height, width)

    rows_per_thread = height // threads

    slices = []
    for i in range(threads):
        start = i * rows_per_thread
        end = (i + 1) * rows_per_thread if i < threads - 1 else height
        slices.append([start, end]) # slices

    return {
        "image": image,
        "slices": slices,
    }


# In[ ]:


def generate_threads(image, slices, worker, args=None):
    if args is None:
        args = []

    new_image = np.zeros_like(image)
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=len(slices)) as executor:
        futures = [
            executor.submit(worker, start, end, lock, new_image, image, *args)
            for start, end in slices
        ]

        for future in futures:
            future.result()
    return new_image


# In[ ]:


def process_image_with_worker(
    worker,
    metadata,
    output_path,
    worker_args=None,
    colored=False,
):
    image_values = get_image_slice_values(metadata, colored=colored)
    image = image_values["image"]
    slices = image_values["slices"]

    args = worker_args(metadata) if callable(worker_args) else (worker_args or [])

    new_image = generate_threads(
        image,
        slices,
        worker,
        args,
    )

    altered_bytes = new_image.tobytes()
    if colored:
        header = f"P6\n{metadata.width} {metadata.height}\n255\n".encode()
    else:
        header = f"P5\n{metadata.width} {metadata.height}\n255\n".encode()

    with open(output_path, "wb") as f:
        f.write(header)
        f.write(altered_bytes)


# In[ ]:


def main():
    metadata, header = start_pipe_reader()


    if header.mode == SLICE_MODE:
        process_image_with_worker(
            threshold_with_slicing_worker,
            metadata,
            output_path="output.pgm",
            worker_args=lambda metadata: [header.slice_range, metadata.maxv],
            colored=header.colored,
        )
    elif header.mode == NEG_MODE:
        process_image_with_worker(
            image_negative_worker,
            metadata,
            output_path="output.ppm",
            colored=header.colored,
        )
    else:
        print("No mode selected!")


# In[ ]:


if __name__ == "__main__":
    main()

