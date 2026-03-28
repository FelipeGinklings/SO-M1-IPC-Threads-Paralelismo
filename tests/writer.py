#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
import numpy as np
import os
from constants import PGM, PIPE_PATH
import json


# In[ ]:


if __name__ == '__main__':
    with Image.open("lena.pgm") as img:
        arr = np.array(img)
        data = arr.tobytes()
        metadata = PGM(img.height, img.width, int(arr.max()), data)


# In[ ]:


#!/usr/bin/env python3

if __name__ == '__main__':
    # Create the named pipe if it doesn't exist
    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)
        print(f"Created named pipe at {PIPE_PATH}")

    print("Writer process started. Opening pipe...")

    # Open the pipe for writing
    with open(PIPE_PATH, 'wb') as pipe:
        message = json.dumps(metadata.to_dict()).encode("utf-8")
        pipe.write(message + b'\n')
        pipe.write(metadata.data)
        pipe.flush()

    print("Writer process finished")

