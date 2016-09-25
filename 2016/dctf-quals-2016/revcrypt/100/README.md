# RevCrypt 100 - Bad OTPxploited

> Writeup by f0xtr0t (Jay Bosamiya)

The [given file](mypam.bin), when opened in IDA Pro, has a function named `mypam_authenticate`. The rest of the functions don't seem to be too useful. So, upon run the HexRays decompiler on it, we get the following (most of it doesn't matter, just pasting it all for completeness):

```
signed __int64 __fastcall mypam_authenticate(__int64 a1, int a2, int a3, __int64 a4)
{
  signed __int64 result; // rax@2
  size_t v5; // rbx@6
  size_t v6; // rax@6
  void *v7; // rsp@6
  __int64 v8; // rbx@8
  size_t v9; // [rsp+0h] [rbp-120h]@6
  __int64 v10; // [rsp+8h] [rbp-118h]@6
  __int64 v11; // [rsp+18h] [rbp-108h]@1
  int v12; // [rsp+20h] [rbp-100h]@1
  int v13; // [rsp+24h] [rbp-FCh]@1
  __int64 v14; // [rsp+28h] [rbp-F8h]@1
  unsigned int v15; // [rsp+30h] [rbp-F0h]@1
  unsigned int v16; // [rsp+34h] [rbp-ECh]@5
  unsigned int v17; // [rsp+38h] [rbp-E8h]@5
  unsigned int v18; // [rsp+3Ch] [rbp-E4h]@5
  char *s2; // [rsp+40h] [rbp-E0h]@3
  char *s1; // [rsp+48h] [rbp-D8h]@1
  time_t timer; // [rsp+50h] [rbp-D0h]@5
  struct tm *v22; // [rsp+58h] [rbp-C8h]@5
  FILE *stream; // [rsp+60h] [rbp-C0h]@6
  size_t v24; // [rsp+68h] [rbp-B8h]@6
  size_t v25; // [rsp+70h] [rbp-B0h]@6
  char *v26; // [rsp+78h] [rbp-A8h]@6
  char s; // [rsp+80h] [rbp-A0h]@5
  char ptr; // [rsp+90h] [rbp-90h]@6
  __int64 v29; // [rsp+F8h] [rbp-28h]@1

  v14 = a1;
  v13 = a2;
  v12 = a3;
  v11 = a4;
  v29 = *MK_FP(__FS__, 40LL);
  v15 = pam_get_user(a1, &s1, "Username: ");
  if ( !strcmp(s1, "dctf") )
  {
    v15 = prompt(v14, "Verification code: ", &s2, 0LL);
    if ( v15 )
    {
      result = v15;
    }
    else
    {
      timer = time(0LL);
      v22 = gmtime(&timer);
      v16 = v22->tm_mday;
      v17 = v22->tm_hour;
      v18 = v22->tm_min;
      sprintf(&s, "mypam%d%d%d", v16, v17, v18);
      if ( !strcmp(&s, s2) )
      {
        stream = fopen("/flag", "r");
        v24 = fread(&ptr, 1uLL, 0x64uLL, stream);
        fclose(stream);
        v5 = strlen(s1);
        v6 = v5 + strlen(&ptr) + 64;
        v25 = v6 - 1;
        v9 = v6;
        v10 = 0LL;
        v7 = alloca(16 * ((v6 + 15) / 0x10));
        v26 = (char *)&v9;
        sprintf((char *)&v9, "Welcome %s! Your flag is: %s\n", s1, &ptr, v6, 0LL);
        prompt(v14, v26, &s2, 0LL);
      }
      result = 7LL;
    }
  }
  else
  {
    result = 7LL;
  }
  v8 = *MK_FP(__FS__, 40LL) ^ v29;
  return result;
}
```

Obviously, by reading this, we notice that the username must be `dctf`, and the verification code must be the `mypam` followed by the day, hour, and minute. Now, there might be a difference in timing (i.e. time skew) between my machine and the server, but I leave that that for later, if it does come up.

Instead, I modify the verification code slightly (to output the verification code, rather than do a `strcmp`) and make a new [C file](verification.c) which I can use to get the verification code.

Now, it comes to _how_ to use the code. Turns out, that PAM means that we just SSH into the given server, and use the username and code we've got.

First off, the VPN thing is a little irritating, but I set it up, and then I try `ssh`ing to the system, but nothing happens. Then I realize that I hadn't specified the user, so upon specifying the user, it asked for verification code, which I provided from the script I'd made, and **BAM!**, it drops the flag. :)