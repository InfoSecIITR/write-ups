# Web/ H34D3RS:
In this challenge we must have a sound knowledge of Headers:

`level1`: user doesn’t seem to be `lorbrowser`
so we set the 

`User-agent:lorbrowser`				

Now when we proceed

`level2`: But wait…. Wlmac people come from vishwactf.com website.Are you a spy?
This is clear indication for use of Referer so we set

`Referer: https://vishwactf.com/`

For the third level

`Level3`: But wait..you are mere mortal who lives in the present. We are divine beings living 20 years in the future. We are not the same. We set the Date Header to 2044

`Date:2044`

Then

`Level4`: But wait...server expressing the clients preference for an encrypted and authenticated response check out it.
Generally the value is 0 or 1 which makes sense. But the author said add a value to the challenge so after bruting the numbers using burp intruer we get 10 as the correct number

`upgrade-insecure-requests:10`

For Next Level

`level5`: But wait..Nine times header field provides the approximate bandwidth of the clients connection to the server

This level just exploded my mind. I asked the author about Downlink and he agreed then after 8 hours he said that downlink is not the answer so I guessed it (I don't know how I guessed it but it was some hint from the author about the delay ig.) but till then I had lost my first blood on this challenge sadly.
So after setting this header

`Downtime:999999999`

Finally got the Flag: `VishwaCTF{s3cret_sit3_http_head3rs_r_c0o1}`
