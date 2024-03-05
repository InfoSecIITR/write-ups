# Intellectual Heir
## Author : Abhishek Mallav

## Source

- You received a package, and you got to know that you are the descendant of RIADSH. There are four files and a safe in the package.

- You should analyze the files, unlock the safe, and prove your worth. The safe has alphanumeric and character combinations.

- PS: The safe has no lowercase buttons.

### FLAG FORMAT:
VishwaCTF{safe's combination}

### Files:
- [package.zip](package.zip)
    - [file.txt](file.txt)
    - [file1.txt](file1.txt)
    - [file2.txt](file2.txt)
    - [Intellectual Heir.py](Intellectual%20Heir.py)

## Encryption

- Understanding the [Intellectual Heir.py](Intellectual%20Heir.py) file
```py
# my secret to hide the combination of my safe in fornt of all without anyone getting a clue what it is ;)

#some boring python function for conversion nothing new
def str_to_ass(input_string):
    ass_values = []
    for char in input_string:
        ass_values.append(str(ord(char)))
    ass_str = ''.join(ass_values)
    return ass_str

input_string = input("Enter the Combination: ")
result = str_to_ass(input_string)
msg = int(result)
```
- This function creates a `ass_str` string with the ascii values of the characters from the `input` string by concatenating.
- Then this function is applied on the `input` string which is the flag and the `result` string is convert into integer.

```py
#not that easy, you figure out yourself what the freck is a & z
a = 
z = 

f = (? * ?) #cant remember what goes in the question mark
e = #what is usually used

#ohh yaa!! now you cant figure out $h!t
encrypted = pow(msg, e, f)
print(str(encrypted))
```
- This seems like the standard RSA encryption.
    - `a` and `z` are primes
    - `f` is `a*z` which is the `modulus`
    - `e` is the exponent which is usually `65537`
    - `encrypted` is the RSA encryption of `m` with `e` and `f`

```py
#bamm!! protection for primes
number = 
bin = bin(number)[2:]

#bamm!! bamm!! double protection for primes
bin_arr = np.array(list(bin), dtype=int)
result = np.sin(bin_arr)
result = np.cos(bin_arr)
np.savetxt("file1", result)
np.savetxt("file2", result)
```
- The last part of the script converts the 2 primes into binary arrays and applies `cos` on one and `sin` on other.

## Decryption
### Scripts
[solve.py](solve.py)

### Explanation
```py
cos = open("file1.txt",'r').read().strip().split('\n')
a = int(''.join(['0' if val[0]=='1' else '1' for val in cos]),2)

sin = open("file2.txt",'r').read().strip().split('\n')
z = int(''.join(['0' if val[0]=='0' else '1' for val in sin]),2)

import sympy
assert sympy.isprime(z)
assert sympy.isprime(a)
```
- First we read the `cos` and `sin` arrays from [file1.txt](file1.txt) and [file2.txt](file2.txt).
- We decode the trigonometric values to get `1` or `0` based on the values in `cos` and `sin` arrays for the binary array of `a` and `z`.
- Then we join the bits and convert it to integer to get `a` and `z`.
- Then we check that `a` and `z` are both primes

```py
f = a*z
e = 65537

c = int(open('file.txt','r').read().strip())
phi = (a-1)*(z-1)
d = pow(e,-1,phi)
m = pow(c,d,f)
```
- Then we read `c` from [file.txt](file.txt) and decrypt the standard RSA

```py
ass_msg = str(m)
msg = ''.join([chr(int(asc)) for asc in [ass_msg[i:i+2] for i in range(0,len(ass_msg),2)]])
print(msg)
```
- Finally, we apply the inverse of `str_to_ass` function to `m` to get the original `msg`.

### Output

```
Y0U_@R3_T#3_W0RT#Y_OF_3
```

## Flag

The Flag is `VishwaCTF{Y0U_@R3_T#3_W0RT#Y_OF_3}`