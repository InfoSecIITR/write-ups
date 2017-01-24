from Crypto.Cipher import AES
from base64 import b64decode

txt=''
f=open('7.txt','r')
for l in f:
	txt+=l.strip()
print txt
txt=b64decode(txt)
key='YELLOW SUBMARINE'
cipher=AES.new(key,AES.MODE_ECB)
msg=cipher.decrypt(txt)
print msg