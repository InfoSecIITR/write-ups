ct = b'mVWAZs_Sj\ni|^\nyzX\x08u\x08vsq~c\nqWulmnali]qsmQb\tmAaUnCvcW\x02'
key = 59
pt = b''.join([(byte ^ key).to_bytes(1,'big') for byte in ct])
print(pt)

import base64
flag = base64.b64decode(pt)
print(flag.decode())