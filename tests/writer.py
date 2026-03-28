#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
import numpy as np
# from dataclasses import dataclass


# In[ ]:


# @dataclass(frozen=True)
# class PGM:
#     height: int
#     width: int
#     maxv: int
#     data: any


# In[ ]:


# #!/usr/bin/env python3
# import os
# import time
# import constants

# # Create the named pipe if it doesn't exist
# if not os.path.exists(constants.PIPE_PATH):
#     os.mkfifo(constants.PIPE_PATH)
#     print(f"Created named pipe at {constants.PIPE_PATH}")

# print("Writer process started. Opening pipe...")

# # Open the pipe for writing
# with open(constants.PIPE_PATH, 'w') as pipe:
#     for i in range(5):
#         message = f"Message {i}: Hello from writer! ({time.time()})\n"
#         print(f"Writing: {message.strip()}")
#         pipe.write(message)
#         pipe.flush()  # Ensure data is written
#         time.sleep(2)

# print("Writer process finished")


# In[ ]:


with Image.open("lena.pgm") as img:
    metadata = {}
    metadata['width'] = img.width
    metadata['height'] = img.height
    arr = np.array(img)
    metadata['maximum_intensity_value'] = int(arr.max())
    metadata['data'] = list(arr)
    print(metadata)

