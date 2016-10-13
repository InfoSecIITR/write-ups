def multi_byte_xor(txt,key):
	j=0
	ans=''
	for c in txt:
		ans+=chr(ord(c)^ord(key[j%len(key)]))
		j=j+1
	return ans.encode('hex')

if __name__ == '__main__':
	expected="0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
	ours=multi_byte_xor("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal",'ICE')

	if (expected==ours):
		print "Easier than the last one!"
