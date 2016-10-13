

def single_byte_xor_key(cipher):   #returns the key
	f=[]
		
	for i in xrange(0,256):
		f.append(0)
		decrypted=''

		for c in cipher:
			decrypted+=chr(i^ord(c))

		for c in decrypted:
			if ((ord(c)>=65 and ord(c)<=90) or (ord(c)>=97 and ord(c)<=122) or ord(c)==32) : #Calculating the no of alphabets in string decrypted with key i
				f[i]+=1

	max_f=0
	key=0
	for i in xrange(0,256):
		if (max_f<f[i]):
			max_f=f[i]
			key=i

	return key

#main starts here
if __name__ == '__main__':
	cipher='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
	cipher=cipher.decode('hex')


	decrypted=''
	key=single_byte_xor_key(cipher)
	for c in cipher:
			decrypted+=chr(key^ord(c))
	print "key",hex(key)
	print decrypted
