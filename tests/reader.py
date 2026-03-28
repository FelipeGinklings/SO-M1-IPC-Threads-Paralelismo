#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import constants
import json


# In[ ]:


#!/usr/bin/env python3

print("Reader process started. Waiting for data...")

# Open the pipe for reading (blocks until writer opens)
with open(constants.PIPE_PATH, 'r') as pipe:
    while True:
        try:
            data = pipe.readline()
            if not data:
                # Pipe was closed by writer
                break
            print(f"Received: {data.strip()}")
            json_string = data.strip()
            data = json.loads(json_string)
            metadata = constants.PGM(data['height'], data['width'], data["maxv"])
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

print("Reader process finished")

