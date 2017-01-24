from base64 import b64encode as be, b64decode as bd

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

def multi_byte_xor(txt,key):  # do the XOR
	j=0
	decrypted=''
	for c in txt:
		decrypted+=chr(ord(c)^ord(key[j%len(key)]))
		j=j+1
	return decrypted


def hamming_dist(a,b):
	count=0
	for i in range(0,len(a)):
		t=bin(ord(a[i])^ord(b[i]))
		for j in range(2,len(t)):
			if (t[j]=='1'):
				count+=1
	return count

def normalized_HD(txt,l):             # calculates av. Normalized Hamming distance
	total_HD=0
	count=0							  #count represent no of pairs which we have checked for total_HD
	for i in range(0,len(txt),2*l):
		if ((i+2*l)<=len(txt)) :
			total_HD+=hamming_dist(txt[i:i+l],txt[i+l:i+2*l])
			count+=1
	#count=len(txt)/l          		 # No of pairs
	avNormalized_HD=1.0*total_HD/(l*count)
	return avNormalized_HD


##main starts here
if __name__ == '__main__':
	f=open('test.txt','r')
	txt=''
	for c in f.read():
		txt+=c

	txt=bd(txt)
	#print txt

	minN_HD=100000
	keylength=0


	for i in range(2,40):
		print i, " : ",normalized_HD(txt,i)
		if (normalized_HD(txt,i)<minN_HD):
			minN_HD=normalized_HD(txt,i)
			keylength=i
	
	#keylength will be the one with min av hamming distance

	print "keylength : ",keylength

	_txt=[]										
	_key=[]

	for i in range(0,keylength):
		_key.append('')
		_txt.append('')

	#Each byte at an interval of keylength is encrypted with single byte i.e it is same single byte xor

	for j in range(0,keylength):
		for i in range(0+j,len(txt),keylength):
			_txt[j]+=txt[i]


	KEY=''
	for j in range(0,keylength):
		_key[j]=single_byte_xor_key(_txt[j])
		KEY+=chr(_key[j])

	print "KEY : ",KEY

	print "----Decoding----"

	print (multi_byte_xor(txt,KEY))

