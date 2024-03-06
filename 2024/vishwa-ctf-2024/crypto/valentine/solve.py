from itertools import cycle
def xor(a, b):
    return [i^j for i, j in zip(a, cycle(b))]

f = open("decrypted.png", "rb").read()
key = [137, 80, 78, 71, 13, 10, 26, 10]
dec = bytearray(xor(f,key))
open('decrypted.png', 'wb').write(dec)
