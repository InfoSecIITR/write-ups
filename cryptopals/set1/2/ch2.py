
buf1=raw_input()
buf2=raw_input()

buf1=(buf1).decode('hex')
buf2=(buf2).decode('hex')

lenght=len(buf1)

ans=''
for i in range(0,lenght):
	ans+=hex(ord(buf1[i])^ord(buf2[i]))[2:]

print ans


