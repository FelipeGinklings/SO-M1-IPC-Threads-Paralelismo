#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
import numpy as np
import os
import constants
import json


# In[ ]:


if __name__ == '__main__':
    with Image.open("lena.pgm") as img:
        arr = np.array(img)
        metadata = {
            "width": img.width,
            "height":img.height, 
            "maximum_intensity_value": int(arr.max()),
        }
        print(metadata)


# In[ ]:


#!/usr/bin/env python3

if __name__ == '__main__':
    # Create the named pipe if it doesn't exist
    if not os.path.exists(constants.PIPE_PATH):
        os.mkfifo(constants.PIPE_PATH)
        print(f"Created named pipe at {constants.PIPE_PATH}")

    print("Writer process started. Opening pipe...")

    # Open the pipe for writing
    with open(constants.PIPE_PATH, 'w') as pipe:
        message = json.dumps(metadata)
        pipe.write(message)
        pipe.flush()

    print("Writer process finished")

