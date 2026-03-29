#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
import numpy as np
import os
from constants import ImageMetadata, Header, PIPE_PATH, NEG_MODE, SLICE_MODE
import json
from tkinter import filedialog
from tkinter import Tk


# In[ ]:


def load_metadata_from_dialog():
    # Hide the main window
    root = Tk()
    root.withdraw()

    # Open file dialog
    image_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Gray image files", "*.pgm"), ("Color image files", "*.ppm")]
    )


    if not image_path:
        print("No file selected")
        return None

    colored = ".ppm" in image_path

    with Image.open(image_path) as img:
        arr = np.array(img)
        data = arr.tobytes()
        return ImageMetadata(img.height, img.width, int(arr.max()), data), colored


# In[ ]:


def load_header_from_input():
    while True:
        try:
            mode = int(input(f"Choose mode ({NEG_MODE}=NEG, {SLICE_MODE}=SLICE): ").strip())
            if mode not in (NEG_MODE, SLICE_MODE):
                print("Invalid mode. Try again.")
                continue

            if mode == NEG_MODE:
                return Header(mode=mode, slice_range=(0, 0))

            start = int(input("Slice start (row index): ").strip())
            end = int(input("Slice end (row index, exclusive): ").strip())
            if start < 0 or end <= start:
                print("Invalid slice range. Use start >= 0 and end > start.")
                continue

            return Header(mode=mode, slice_range=(start, end))
        except ValueError:
            print("Please enter integer values.")


# In[ ]:


def ask_metadata_and_start_pipe(metadata, header):
    if metadata is None or header is None:
        return

    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)
        print(f"Created named pipe at {PIPE_PATH}")

    print("Writer process started. Opening pipe...")

    with open(PIPE_PATH, "wb") as pipe:
        payload = metadata.to_dict()
        payload["header"] = header.to_dict()
        message = json.dumps(payload).encode("utf-8")
        pipe.write(message + b"\n")
        pipe.write(metadata.data)
        pipe.flush()

    print("Writer process finished")


# In[ ]:


def main():
    metadata, colored = load_metadata_from_dialog()
    if metadata:
        header = load_header_from_input()
        header.colored = colored
        ask_metadata_and_start_pipe(metadata, header)


# In[ ]:


if __name__ == "__main__":
    main()

