cos = open("file1.txt",'r').read().strip().split('\n')
a = int(''.join(['0' if val[0]=='1' else '1' for val in cos]),2)

sin = open("file2.txt",'r').read().strip().split('\n')
z = int(''.join(['0' if val[0]=='0' else '1' for val in sin]),2)

import sympy
assert sympy.isprime(z)
assert sympy.isprime(a)

f = a*z
e = 65537

c = int(open('file.txt','r').read().strip())
phi = (a-1)*(z-1)
d = pow(e,-1,phi)
m = pow(c,d,f)

ass_msg = str(m)
msg = ''.join([chr(int(asc)) for asc in [ass_msg[i:i+2] for i in range(0,len(ass_msg),2)]])
print(msg)