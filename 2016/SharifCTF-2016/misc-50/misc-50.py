
from playfake import get_pos,get_letter,make_key,make_message,playfair_enc,make_flag

def decrypt(ctxt, key):
	msg=''
	for i in range(0, len(ctxt), 2):
		r0, c0 = get_pos(key, ctxt[i])
		r1, c1 = get_pos(key, ctxt[i+1])
		if r0 == r1:
			msg += get_letter(key, (r0-1)%5, (c0-1)%5) + get_letter(key, (r1-1)%5, (c1-1)%5)
		elif c0 == c1:
			msg += get_letter(key, (r0+1)%5, (c0+1)%5) + get_letter(key, (r1+1)%5, (c1+1)%5)
		else:
			msg += get_letter(key, (r0-1)%5, (c1+1)%5) + get_letter(key, (r1-1)%5, (c0+1)%5)
	return msg


cipher = 'KPDPDGYJXNUSOIGOJDUSUQGFSHJUGIEAXJZUQVDKSCMQKXIR'
f = '/etc/dictionaries-common/words'

possible_words = []

for word in open(f, 'r'):
	if (len(word.strip()) == 5 and word.strip().find("'") == -1):
		possible_words.append(word.strip())

possible_key1=[]
print 'For "SharifCTF" phrase , brute-forcing ...'
for word in possible_words:
	key=make_key(word)
	msg2 = make_message('SharifCTF')
	ctxt = playfair_enc(key, msg2)

	if (ctxt[:-2] in cipher):
		print 'Found : ',word
		possible_key1.append(word)

print 'Found : ',possible_key1


possible_key2 = []

print 'For "Contest" phrase , brute-forcing ...'
for word in possible_words:
	key=make_key(word)
	msg2 = make_message('ontest')
	ctxt = playfair_enc(key, msg2)

	if (ctxt[:-2] in cipher):
		print 'Found : ',word
		possible_key2.append(word)

print 'Found : ',possible_key2

print '\nIntersection of possible_key1,possible_key2 will be the KEY\n'
#Intersection of possible_key1,2
key = 'BROWN'
print 'KEY : ',key,'\n'

print decrypt('KPDPDGYJXNUSOIGOJDUSUQGFSHJUGIEAXJZUQVDKSCMQKXIR', make_key(key))

print 'After modification msg : '+'CURRENTLYTHESEVENTHSHARIFCTFCONTESTISBEINGHELD'

print 'Flag : '+make_flag('CURRENTLYTHESEVENTHSHARIFCTFCONTESTISBEINGHELD')

