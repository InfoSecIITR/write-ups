# HAPPY VALENTINE'S DAY

## Author : Pushkar Deore

### DESCRIPTION :
My girlfriend and I captured our best moments of Valentine's Day in a portable graphics network. But unfortunately I am not able to open it as I accidentally ended up encrypting it. Can you help me get my memories back?

### Files:
* [enc.txt](enc.txt) 
* [source.txt](source.txt)

### Analysis : 
* After analysing the source.txt we got that a png image is getting encrypted by simple xor where the key are the first 8 header of a png file
* And if you know a little about png files you would know that all png files have the same first 8 headers that are [137, 80, 78, 71, 13, 10, 26, 10]
* So we can decrypt the enc.txt with this script

```python
from itertools import cycle
def xor(a, b):
    return [i^j for i, j in zip(a, cycle(b))]

f = open("decrypted.png", "rb").read()
key = [137, 80, 78, 71, 13, 10, 26, 10]
dec = bytearray(xor(f,key))
open('decrypted.png', 'wb').write(dec)
```

* On running this we got the decrypted.png

![alt text](decrypted.png)

* So our flag is 
'VishwaCTF{h3ad3r5_f0r_w1nn3r5}'