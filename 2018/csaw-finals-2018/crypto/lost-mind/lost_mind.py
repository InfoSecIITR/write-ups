import gmpy2
import sys
import itertools
import re

from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from  pwn import *

l=[0]

def lsb_oracle(bits,n):
	beg=0
	end=n-1
	for i in bits:
		mid=(beg+end)/2
		if not i:
			end=mid
		else:
			beg=mid
	return long_to_bytes(end),long_to_bytes(beg)

def encrypt(data):
	l[0]+=1
	r.recvuntil("=\n")
	r.recvuntil("=\n")
	r.sendline("1")
	r.recvuntil("input:")
	r.sendline(data)
	return r.recvline().strip()

def decrypt(data):
	l[0]+=1
	r.recvuntil("=\n")
	r.recvuntil("=\n")
	r.sendline("2")
	r.recvuntil("input:")
	r.sendline(data)
	return r.recvline().strip()	


def recover_flag(enc, dec, flag, n):
    x = flag
    bits = []
    lastchar = int(dec(long_to_bytes(flag)), 16)
    print lastchar
    prev = lastchar
    multiplier = int(enc(long_to_bytes(2 ** 8)), 16)
    try:
        for i in range(128):
            x = (x * multiplier)%n
            expected_value = int(dec(long_to_bytes(x)), 16)
            real_x = prev
            for configuration in itertools.product([0, 1], repeat=8):
                res = real_x % 256
                for bit in configuration:
                    res = res * 2
                    if bit == 1:
                        res = res - n
                res = res % 256
                if res == expected_value:
                    bits.extend(configuration)
                    break
            prev = expected_value
    except:
        pass
    return lsb_oracle(bits,n)[0][0]

def recover_pubkey(enc):
    two = int(enc('\x05'), 16)
    three = int(enc('\x07'), 16)
    power_two = int(enc('\x19'), 16)
    power_three = int(enc('\x31'), 16)
    n = gmpy2.gcd(two ** 2 - power_two, three ** 2 - power_three)

    while n % 2 == 0:
        n = n / 2
    while n % 3 == 0:
        n = n / 3
    while n % 5 == 0:
        n = n / 5
    while n % 7 == 0:
        n = n / 7

    return n

D=[]
for i in xrange(len(flag),40):
	d=[]
	try:
		for j in xrange(10):
			r = remote("crypto.chal.csaw.io",1003)
			l=[0]
			r.recvuntil("len:")
			r.sendline("{},1".format(str(i)))
			r.recvuntil("encrypted flag: ")
			flag = int(r.recvline().strip(),16)
			n = recover_pubkey(encrypt)
			t=recover_flag(encrypt,decrypt,flag,n)
			d.append(t[0])
			print d,i
	except Exception as e:
		print d,e
	D.append(d)
	print d
print D

flag = ''.join([max(i,key=lambda x:i.count(x)) for i in D])

print flag