from towers import fixer
from pwn import *
from time import sleep

conn = remote('78.46.224.71', 14449)

data = fixer(8,1,2,3)
data2 = data[-2:]
data = data[:-2]

for i in range(0, len(data), 5000):
    print len(data[i:i+5000])

dmanager = [data[i:i+5000] for i in range(0, len(data), 5000)]

print conn.recv()
conn.sendline('S')
sleep(2)
print conn.recv()

for d in dmanager:
    conn.sendline(d)
    sleep(2)
    print conn.recv()

conn.interactive()

