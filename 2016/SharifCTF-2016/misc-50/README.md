## PlayFake (Misc-50)

### Description

# See `playfake.py` and decrypt the ciphertext

Ciphertext = KPDPDGYJXNUSOIGOJDUSUQGFSHJUGIEAXJZUQVDKSCMQKXIR

# Notice that flag is generated using "msg", not "msg2".
# After decryption, you get "msg2".
# You must manually add spaces and perform other required changes to get "msg".

### Solution
* It is given that the words `SharifCTF` and `contest` exits in the `msg`
* Also msg2 and msg are almost identical.
* So, I brute-force the 5-letter long key using all the meaningful 5-letter words
* How did I do that?
* If I calculate cipher corresponding to `SharifCTF`, then it must be present in Ciphertext
* I take `SharifCTF` as msg and calculated cipher and check for whick keys it is in Ciphertext
* Similarly I do for `contest`, then I take intersection of possible keys in two cases
* After calculating the key, writing decryption is easy and calculate `msg2`.
* After that msg with a few modification.
* Passing msg to `make_flag()` gives away the flag.
* `SharifCTF{655ad15484a60457f3af49512a5d5206}`