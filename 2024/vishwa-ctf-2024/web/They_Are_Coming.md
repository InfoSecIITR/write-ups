# They are Coming 
Web(200 points)

**DESCRIPTION**
> Aesthetic Looking army of 128 Robots with AGI Capabilities are coming to destroy our locality!

The description hints at Robots.txt.
By going on /robots.txt, we get the following :

```
# https://www.robotstxt.org/robotstxt.html
User-agent: *
Disallow: /admin
L3NlY3JldC1sb2NhdGlvbg==
Decryption key: th1s_1s_n0t_t5e_f1a9
```
Decoding the base64 string, we get : `/secret-location`
Going to /secret-location, if we check out local-storage, we find a secret-key:
>Gkul0oJKhNZ1E8nxwnMY8Ljn1KNEW9G9l+w243EQt0M4si+fhPQdxoaKkHVTGjmA

The page of /secret-location shows this ,hinting to AES-128
![image](https://github.com/ayu-ch/VishwaCTF-writeup/assets/137001939/740fe627-0848-4867-b9cc-6652427d698a)

Now we have the secret-key and the decryption-key, by using AES-12-CBC decryption, we get the flag
>**VishwaCTF{g0_Su88m1t_1t_Qu14kl7}**
