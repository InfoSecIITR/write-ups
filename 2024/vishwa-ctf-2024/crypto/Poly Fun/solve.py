rev = dict()
for i in range(256):
    rev[4*i**2+3*i+7] = i

enc_key = open('encoded_key.txt','r').read()
key = b''.join([(rev[ord(char)]).to_bytes(1,'big') for char in enc_key])

print(key)

enc_flag = open('encoded_flag.txt','rb').read()

import base64
ct = base64.b64decode(enc_flag)

from Crypto.Cipher import AES
cipher = AES.new(key,AES.MODE_ECB)
print(cipher.decrypt(ct).decode().strip())