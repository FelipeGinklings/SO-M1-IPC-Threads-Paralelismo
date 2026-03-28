#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from constants import PIPE_PATH, PGM
import json


# In[ ]:


#!/usr/bin/env python3

if __name__ == "__main__":
    print("Reader process started. Waiting for data...")

    # Open the pipe for reading (blocks until writer opens)
    metadata_dict = {}
    pixel_bytes = b""
    with open(PIPE_PATH, "rb") as pipe:
        while True:
            try:
                metadata = pipe.readline()
                if not metadata:
                    # Pipe was closed by writer
                    break
                metadata_dict = json.loads(metadata.decode())
                pixel_bytes = pipe.read(
                    metadata_dict["width"] * metadata_dict["height"]
                )
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                break
    print(metadata_dict, f", Bytes len: {len(pixel_bytes)}")

    print("Reader process finished")

