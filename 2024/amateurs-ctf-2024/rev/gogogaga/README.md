# gogogaga
created by flocto

## Challenge
> "wow its my favorite language to rev" - nobody  
`nc chal.amt.rs 2200`

#### Downloads
[main](./files/main)


## Solution

Let's see what type of binary we are provided with.

`$ file main`  

`main: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=qXgpNaa6CA-hMFGspCIU/iDmVzP5EhqshPquYFC-C/xlqOk9gfHBc2_a52vYID/fjCleY4wHB8pzpHw6Yk5, with debug_info, not stripped`


It's an ELF64 golang binary. Using IDA Free 8.4 to decompile this, we can find the `main_main` function.

```go
// main.main
void __fastcall main_main()
{
  retval_487120 File; // [rsp-28h] [rbp-A8h] BYREF
  _QWORD v1[2]; // [rsp+28h] [rbp-58h] BYREF
  _QWORD v2[2]; // [rsp+38h] [rbp-48h] BYREF
  _QWORD v3[2]; // [rsp+48h] [rbp-38h] BYREF
  _QWORD v4[2]; // [rsp+58h] [rbp-28h] BYREF
  _QWORD v5[3]; // [rsp+68h] [rbp-18h] BYREF
  io_Writer v6; // 0:rax.8,8:rbx.8
  io_Writer v7; // 0:rax.8,8:rbx.8
  io_Reader v8; // 0:rax.8,8:rbx.8
  io_Writer v9; // 0:rax.8,8:rbx.8
  io_Writer v10; // 0:rax.8,8:rbx.8
  string v11; // 0:rax.8,8:rbx.8
  io_Writer v12; // 0:rax.8,8:rbx.8
  _slice_interface_ v13; // 0:rcx.8,8:rdi.16
  _slice_interface_ v14; // 0:rcx.8,8:rdi.16
  _slice_interface_ v15; // 0:rcx.8,8:rdi.16

  v5[0] = &RTYPE_string_0;
  v5[1] = &off_4D4BF8;
  v6.data = os_Stdout;
  v6.tab = (runtime_itab *)&go_itab__ptr_os_File_comma_io_Writer;
  v13.array = (interface_ *)v5;
  v13.len = 1LL;
  v13.cap = 1LL;
  fmt_Fprintln(v6, v13);
  v4[0] = &RTYPE_string_0;
  v4[1] = &off_4D4C08;
  v7.data = os_Stdout;
  v7.tab = (runtime_itab *)&go_itab__ptr_os_File_comma_io_Writer;
  v13.array = (interface_ *)v4;
  v13.len = 1LL;
  v13.cap = 1LL;
  fmt_Fprint(v7, v13);
  File._r0_2.cap = (int)runtime_newobject((internal_abi_Type *)&RTYPE_string_0);
  *(_QWORD *)File._r0_2.cap = 0LL;
  v3[0] = &RTYPE__ptr_string;
  v3[1] = File._r0_2.cap;
  v8.data = os_Stdin;
  v13.array = (interface_ *)v3;
  v13.len = 1LL;
  v13.cap = 1LL;
  v8.tab = (runtime_itab *)&go_itab__ptr_os_File_comma_io_Reader;
  fmt_Fscanln(v8, v13);
  if ( main_checkKey(*(string *)File._r0_2.cap) )
  {
    v2[0] = &RTYPE_string_0;
    v2[1] = &off_4D4C18;
    v9.data = os_Stdout;
    v9.tab = (runtime_itab *)&go_itab__ptr_os_File_comma_io_Writer;
    v14.array = (interface_ *)v2;
    v14.len = 1LL;
    v14.cap = 1LL;
    fmt_Fprintln(v9, v14);
    v1[0] = &RTYPE_string_0;
    v1[1] = &off_4D4C28;
    v10.data = os_Stdout;
    v10.tab = (runtime_itab *)&go_itab__ptr_os_File_comma_io_Writer;
    v14.array = (interface_ *)v1;
    v14.len = 1LL;
    v14.cap = 1LL;
    fmt_Fprint(v10, v14);
    v11.str = (uint8 *)"flag.txt";
    v11.len = 8LL;
    File = os_ReadFile(v11);
    File._r1_2.tab = (runtime_itab *)&RTYPE_string_0;
    File._r1_2.data = &off_4D4C38;
    v11.len = (int)os_Stdout;
    v11.str = (uint8 *)&go_itab__ptr_os_File_comma_io_Writer;
    v14.array = (interface_ *)&File._r1_2;
    v14.len = 1LL;
    v14.cap = 1LL;
    fmt_Fprintln((io_Writer)v11, v14);
  }
  else
  {
    File._r1.tab = (runtime_itab *)&RTYPE_string_0;
    File._r1.data = &off_4D4C48;
    v12.data = os_Stdout;
    v12.tab = (runtime_itab *)&go_itab__ptr_os_File_comma_io_Writer;
    v15.array = (interface_ *)&File._r1;
    v15.len = 1LL;
    v15.cap = 1LL;
    fmt_Fprintln(v12, v15);
  }
}
```

Let's ignore the redundant stuff and focus on the main part. First, we need to resolve all the strings (`&off_hex`) using the `.rodata` section to get the correct value for `fmt_Fprint`.

Highlighting only the important stuff:

```go
// main.main
void __fastcall main_main()
{
  ...
  fmt_Fprintln(v6, v13); // Gimme a key
  ...
  fmt_Fprint(v7, v13); // >
  ...
  // get the input
  fmt_Fscanln(v8, v13);
  // check the input using `main_checkKey` function
  if ( main_checkKey(*(string *)File._r0_2.cap) )
  {
    ...
    fmt_Fprintln(v9, v14); // Looks good to me!
    ...
    fmt_Fprint(v10, v14); // Here's your flag: 
     // read flag.txt
    v11.str = (uint8 *)"flag.txt";
    File = os_ReadFile(v11);
    ...
    // print the contents
    fmt_Fprintln((io_Writer)v11, v14);
  }
  else
  {
    ...
    fmt_Fprintln(v12, v15); // Try again!
  }
}
```

It's clear that we just need the `main_checkKey` function to return true for a certain key that we need to find.