# Poly Fun
## Author : Revak Pandkar

## Source

- Its a simple symmetric key encryption, I am sure you will be able to solve it (what do you mean the key looks weird)

### Files:
- [challenge.py](challenge.py)
- [encoded_flag.txt](encoded_flag.txt)
- [encoded_key.txt](encoded_key.txt)

## Encryption

- Understanding the [challenge.py](challenge.py) file
```py
import numpy as np
import random

polyc = [4,3,7]
poly = np.poly1d(polyc)


def generate_random_number():
    while True:
        num = random.randint(100, 999)
        first_digit = num // 100
        last_digit = num % 10
        if abs(first_digit - last_digit) > 1:
            return num


def generate_random_number_again():
    while True:
        num = random.randint(1000, 9999)
        if num % 1111 != 0:
            return num
```
- A function poly has been created which returns `4*x**2+3*x+7` for the parameter `x` provided

- Two random number generator functions have been defined with a condition for the return value of either. This comes into play in the `transform` function

- The `transform` function _ is an identity.
- Every if else condition in the function is either a tautology or a contradiction in the given context.
- Whichever group of number will give a different result has been removed from the possibility in the RNG functions.

- On erasing impossible cases, `transform(i)` returns `i` in the end.

```py
def encrypt(p,key):
    return ''.join(chr(p(transform(i))) for i in key)


key = open('key.txt', 'rb').read()
enc = encrypt(poly,key)
print(enc)
```

- The program reads `key.txt` and encrypts each character in the bytestring.
- The encrypt function applies the `poly` function on the ascii value of the byte and adds the `chr()` of the result to the result.

## Decryption
### Scripts
[solve.py](solve.py)

### Explanation
- The file `key.txt` is being read as bytes, so every byte can only be in range 0 to 255.
- So I mapped every character with its result when passed into that polynomial, so that we can simply reverse each mapping to get back the original byte.

- The characters in [encoded_key.txt](encoded_key.txt) had huge ascii values so I assumed those were encoded using this polynomial.
- If i read them as bytes, they would break into bytes of size 8 bits so i read then as a string and reversed the encoding.

```py
rev = dict()
for i in range(256):
    rev[4*i**2+3*i+7] = i

enc_key = open('encoded_key.txt','r').read()
key = b''.join([(rev[ord(char)]).to_bytes(1,'big') for char in enc_key])

print(key)
```

- The `key` turned out to be 32 bytes long.
- The content in [encoded_flag.txt](encoded_flag.txt) was clearly base64 encoded, which on decoding returned a 48 byte long bytestring.
- 16 byte multiplicity was there so I decrypted the base64 decoded content of [encoded_flag.txt](encoded_flag.txt) using the `key` in `AES`.

```py
enc_flag = open('encoded_flag.txt','rb').read()

import base64
ct = base64.b64decode(enc_flag)

from Crypto.Cipher import AES
cipher = AES.new(key,AES.MODE_ECB)
print(cipher.decrypt(ct).decode().strip())
```

### Output

```
b'12345678910111213141516171819202'
VishwaCTF{s33_1_t0ld_y0u_1t_w45_345y}
```

## Flag

The Flag is `VishwaCTF{s33_1_t0ld_y0u_1t_w45_345y}`