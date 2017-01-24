
def score(txt):
	txt=txt[0:len(txt)-1].decode('hex')
	
	count=0
	for i in range(0,len(txt),16):				#No of 16_byte strings which EXACTLY matches with some other 16_byte string
		for j in range(i+16,160,16):
			if (txt[i:i+16]==txt[j:j+16]):
				count+=1
	return count


##main starts here
if __name__ == '__main__':
	f=open('8.txt','r')
	noOfMatches=0								
	ans=''
	for txt in f: 
		if (score(txt)>noOfMatches):
			noOfMatches=score(txt)
			ans=txt

	print ans