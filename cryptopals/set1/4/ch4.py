
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
	engf=[]
	for i in range(0,256):
		engf.append(0)

	engf[97:123]=[8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.768,0.978,2.36,0.15,1.974,0.074]
	engf[65:91]=[8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.768,0.978,2.36,0.15,1.974,0.074]
	engf[32]=16.33

	maxALPHANUMERIC=0
	ans=''
	for buf in open('4.txt','r'):
		
		buf=buf[0:len(buf)-1].decode('hex')

		key=single_byte_xor_key(buf)
		decrypted=''

		current_max_ALPHANUMERIC=0
		for c in buf:
			decrypted+=chr(key^ord(c))
			if ((ord(c)>=65 and ord(c)<=90) or (ord(c)>=97 and ord(c)<=122) or ord(c)==32) :
				current_max_ALPHANUMERIC+=1

		if (current_max_ALPHANUMERIC>maxALPHANUMERIC) :
			maxALPHANUMERIC=current_max_ALPHANUMERIC
			ans=decrypted

	print ans,