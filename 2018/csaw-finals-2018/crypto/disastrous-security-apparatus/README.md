# Crypto 400 - Disastrous Security Apparatus

> Writeup by Aditya Gupta

## Server: [main.py](main.py)

We are given a Flask web server that allows to sign any data using DSA with SHA1 hashes. It gives flag when we submit a valid signature of a valid Fernet ciphertext but the hash algorithm here is SHA256. We can retrieve the `public_key` too.

We also have a forgot password feature where we can obtain any number of random 64 bit integers from the built-in `random` module. 

```python
@app.route("/forgotpass")
def returnrand():
    # Generate a random value for the reset URL so it isn't guessable
    random_value = binascii.hexlify(struct.pack(">Q", random.getrandbits(64)))
    return "https://innitech.local/resetpass/{}".format(
        random_value.decode("ascii")
    )
```

The random k value in `sign` is also generated using the built-in `random` module. 

```python
@app.route("/sign/<data>")
def signer(data):
    r, s = sign(ctf_key, data)
    return json.dumps({"r": r, "s": s})

def sign(ctf_key, data):
    data = data.encode("ascii")
    pn = ctf_key.private_numbers()
    g = pn.public_numbers.parameter_numbers.g
    q = pn.public_numbers.parameter_numbers.q
    p = pn.public_numbers.parameter_numbers.p
    x = pn.x
    k = random.randrange(2, q)
    kinv = _modinv(k, q)
    r = pow(g, k, p) % q
    h = hashlib.sha1(data).digest()
    h = int.from_bytes(h, "big")
    s = kinv * (h + r * x) % q
    return (r, s)
```

We can call `forgotpass` any number of times and guess the internal state of the PRNG using [`randcrack`](https://github.com/tna0y/Python-random-module-cracker). 

```python
def getrand64():
	temp = rq.get(url+"forgotpass").text.split("/")[-1]
	return struct.unpack(">Q",binascii.unhexlify(temp))[0]

rc = RandCrack()

for i in range(624//2):
	print (i)
	temp = getrand64()
	rc.submit(temp&0xffffffff)
	rc.submit(temp>>32)
```

Now we can call `sign` and guess the `k` value. Knowing `k` completely breaks DSA as we can retrieve the private-key `x` from the following steps.

We know all values in the equation except `x`.

![](https://latex.codecogs.com/gif.latex?s%20%5Cequiv%20k%5E%7B-1%7D%5C%2C%28h&plus;r*x%29%5C%2C%20mod%5C%2C%20q)

Rewriting this as

![](https://latex.codecogs.com/gif.latex?x%5C%2C%20%5Cequiv%20r%5E%7B-1%7D%5C%2C%28s*k-h%29%5C%2Cmod%5C%2C%20q)

we can get `x`.

```python
def getx(pk):
	h = hashlib.sha1("AAAA".encode("ascii")).digest()
	h = int.from_bytes(h, "big")
	g=pk['g']
	q=pk['q']
	p=pk['p']
	sig = sign()
	s=sig['s']
	r=sig['r']
	k=rc.predict_randrange(2,q)
	x=int((s*k-h)*gmpy2.invert(r,q) % q)
	return x
```

The only problem was that the request for forgot password had to be sent without any interruption as there were no seperate sessions. After a few tries though we were able to successfully create an accurate `rc` and get `x`.
 
```python
key = DSA.construct((y,g,p,q,x))
pem_data=(key.exportKey())
ctf_key = load_pem_private_key(
    pem_data, password=None, backend=default_backend()
)

data = challenge().encode("ascii")
sig = binascii.hexlify(ctf_key.sign(data,hashes.SHA256()))

print (sig,data)
print (rq.post(url+"capture",data={"signature":sig,"challenge":data}).text)
```

After this we only need to sign a `challenge` and capture the flag.

