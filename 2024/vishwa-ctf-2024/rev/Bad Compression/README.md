# Bad Compression
## Author : Saksham Saipatwar

## Source

- Mr. David was a student pursuing Doctorate of Science in MIT . He was developing a compression algorithm and wrote a code for the same and tested it by encoding a document ... which was successfully Encoded . But he mistakenly deleted that document , can you help him retrieve this document from its encoded file ... you can refer to his code and his diary.

### Files:
- [compress.exe](compress.exe)
- [Diary.jpg](Diary.jpg)
- [Encoded.txt](Encoded.txt)

## Reversing

### Tools Used
- [pyinstxtractor.py](pyinstxtractor.py)
- [pycdc.exe](pycdc.exe)
- [pycdas.exe](pycdas.exe)

### Extracted Files
- [compress.pyc](compress.pyc)
- [compress.py](compress.py)
- [assembly.txt](assembly.txt)

### Final script
- [solve.py](solve.py)

### Extracting the Python Code

- I used [pyinstxtractor.py](pyinstxtractor.py) to extract the [compress.pyc](compress.pyc) file from [compress.exe](compress.exe)
``` bash
akslegion@finallynoti3:/mnt/c/Users/atish/Downloads/crypto/vishwa/rev$ python3 pyinstxtractor.py compress.exe 
[+] Processing compress.exe
[+] Pyinstaller version: 2.1+
[+] Python version: 3.12
[+] Length of package: 7705149 bytes
[+] Found 60 files in CArchive
[+] Beginning extraction...please standby
[+] Possible entry point: pyiboot01_bootstrap.pyc
[+] Possible entry point: pyi_rth_inspect.pyc
[+] Possible entry point: compress.pyc
[!] Warning: This script is running in a different Python version than the one used to build the executable.
[!] Please run this script in Python 3.12 to prevent extraction errors during unmarshalling
[!] Skipping pyz extraction
[+] Successfully extracted pyinstaller archive: compress.exe

You can now use a python decompiler on the pyc files within the extracted directory
```

- I tried using [pycdc.exe](pycdc.exe) to decompile the [compress.pyc](compress.pyc) file to get the python code, but the bytecode provided is from `Python3.12` as extracted by [pycdc.exe](pycdc.exe). So [pycdc.exe](pycdc.exe) wasn't able to decompile the code properly and it provided a broken python code without any function implementation.
- Broken python code is in [compress.py](compress.py)
``` bash
akslegion@finallynoti3:/mnt/c/Users/atish/Downloads/crypto/vishwa/rev$ ./pycdc.exe compress.pyc >> compress.py
Unsupported opcode: COPY
Unsupported opcode: JUMP_BACKWARD
Unsupported opcode: JUMP_BACKWARD
Unsupported opcode: POP_JUMP_IF_NOT_NONE
Unsupported opcode: JUMP_BACKWARD
Unsupported opcode: BEFORE_WITH
Unsupported opcode: BEFORE_WITH
```

- So I used [pycdas.exe](pycdas.exe) to get the assembly code from [compress.pyc](compress.pyc) and stored it in [assembly.txt](assembly.txt)
```bash
akslegion@finallynoti3:/mnt/c/Users/atish/Downloads/crypto/vishwa/rev$ ./pycdas.exe compress.pyc >> assembly.txt
```

- On Reading the assembly code, it was an implementation of `Huffman Encoding` with one change.
    - Instead of using the `frequency` as values for the binary tree, `frequency + ord(char)%7` was used.

```
                82      LOAD_FAST                       0: freq
                84      LOAD_GLOBAL                     7: NULL + ord
                94      LOAD_FAST                       2: char
                96      CALL                            1
                104     LOAD_CONST                      1: 7
                106     BINARY_OP                       6 (%)
                110     BINARY_OP                       0 (+)
```

- Now I used `AI-Tools` - Chat-GPT and a bit of error fixing from my side on the code returned from Chat-GPT to create the python code [solve.py](solve.py)

### Decoding the Huffman Encoding
- On Checking [Diary.jpg](Diary.jpg), it contained the characters in the flag and their frequency, which was Huffman Encoded to get [Encoded.txt](Encodec.txt)

- So I Encoded a string with all the characters with the same frequency as given in [Diary.jpg](Diary.jpg). This will form the dictionary of codes for each character.
- Had to make the map `mp` global so that the data can be used in the `main` function too.

```py
data = "000000_____3333CCCCDDDDNNNN44477UU5AFHKRTVWYahisw{}"
data = trim(data)
encode(data)
print(mp)
```

- Then I reversed the `map` and used it to replace the sections of [Encoded.txt](Encoded.txt) and retrieve the characters of the `flag`
```py
l = 0
r = 1
enc = '110111011011111110101110001110111110110000100011011110111011110011010110001111011011101000101000110011101000000101111101000000000101101000111001011000100010011010010110000101000010110100110111111101101011011111101110001000111001011011001'
dec = ''
imp = dict()
for i in mp:
    imp[mp[i]] = i
while r<=len(enc):
    if enc[l:r] in imp:
        dec+=imp[enc[l:r]]
        l=r
    r+=1
print(dec)
```
- The output came out jumbled so now all that was left was to guess the order of the flag.
- I probably didn't decompile it perfectly 😅.

### Output

``` 
VisaT}CwF{C0N4KH75_Y0U_D3C0D3D_7A3_UNRN0WN404_C0D3h
```

## Flag

- The Flag is `VishwaCTF{C0N4RA75_Y0U_D3C0D3D_7H3_UNKN0WN404_C0D3}`