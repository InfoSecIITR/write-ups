Rev/Sandese Aate Hai Writeup -->


The actual challenge was that we had to understand the operation performed on the given matrix and then perform them in reverse order to obtain the matrix but the author just gave the flag in hardcoded form so made our work quite easy 

__int64 __fastcall sub_17DE(int a1, int a2)
{
int v3[36]; // [rsp+8h] [rbp-90h]

v3[0] = 86;
v3[1] = 105;
v3[2] = 115;
v3[3] = 104;
v3[4] = 119;
v3[5] = 97;
v3[6] = 100;
v3[7] = 50;
v3[8] = 51;
v3[9] = 121;
v3[10] = 51;
v3[11] = 67;
v3[12] = 110;
v3[13] = 50;
v3[14] = 107;
v3[15] = 48;
v3[16] = 118;
v3[17] = 84;
v3[18] = 52;
v3[19] = 52;
v3[20] = 125;
v3[21] = 118;
v3[22] = 49;
v3[23] = 70;
v3[24] = 95;
v3[25] = 109;
v3[26] = 95;
v3[27] = 104;
v3[28] = 99;
v3[29] = 123;
v3[30] = 121;
v3[31] = 51;
v3[32] = 50;
v3[33] = 100;
v3[34] = 110;
v3[35] = 52;
return (unsigned int)v3[6 * a1 + a2];
}

On converting these ascii codes to characters we get 

![alt text](<Screenshot 2024-03-06 090753-1.png>)

Now on arranging these in a matrix form we get 

![alt text](<Screenshot 2024-03-06 091246-1.png>)

And after this using the matrix logic of the code it is clear we have to obtain the flag by going in a spiral fashion and we get our flag as 

`VishwaCTF{4nd23y_4nd23y3v1ch_m42k0v}`