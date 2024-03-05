# BitBane - Cryptic Chaos
## Author : Saksham Saipatwar

## Source

- Once again, Mr. David made a blunder by encrypting some confidential data and deleting the original file. Can you help him retrieve the data from the encrypted file?

### Files:
- [Encrypt.cpp](Encrypt.cpp)
- [Encrypted.txt](Encrypted.txt)

## Encryption
- We will go in sequential order in [Encrypt.cpp](Encrypt.cpp) to understand the encryption.

``` cpp
int main()
{
    fstream file;
    file.open("Flag.txt");
    string data;
    file >> data;
    file.close();
    vector<int> encryption;
    string key = "VishwaCTF";
    encode(encryption, data, key);
    applyKey(encryption, key);
    extraSecurity(encryption);
    writeToFile(encryption);
    return 0;
}
```
- To start with the flag string is being read into `data` from `Flag.txt`
- Firstly the `data` and `key` were used to create the `encryption` vector using the `encode` function.
- Secondly `applykey` function is used on the `encryption` vector.
- Lastly `extrasecurity` function is applied on the `encryption` vector and it is stored in [Encrypted.txt](Encrypted.txt)

``` cpp
int create(int curr, int idx)

void encode(vector<int> &encryption, const string &data, string &key)
{
    int len = data.length();
    for (int i = 0; i < len; ++i)
    {
        int curr = data[i];
        int idx = (i % 8) + 2;
        int num = create(curr, idx);
        encryption.push_back(num);
    }
}
```
- Looking at the First step to create the `encryption` vector
- For every character in the string `data`, the value of that character, `curr` and using it's index, `i % 8 +2` are passed into the function `create`, which returns an integer `num`, which is pushed into the `encryption` vector.
- We don't need to go into the details of `create` as we can easily brute it.

``` cpp
void applyKey(vector<int> &encryption, string &key)
{
    int n = key.size();
    for (int i = 0; i < n; ++i)
    {
        int curr = key[i];
        int cnt = 0;
        int cpy = curr;
        while (cpy)
        {
            if (cpy & 1)
                ++cnt;
            cpy = cpy >> 1;
        }
        curr = curr << (i + 10);
        while (cnt--)
        {
            curr = curr << 1;
            curr = curr ^ 1;
        }
        int k = encryption.size();
        for (int j = 0; j < k; ++j)
        {
            encryption[j] = encryption[j] ^ curr;
        }
    }
}
```
- Now looking into the 2nd function, `applyKey`, every byte of the string `key` goes through some specific changes and then the final value of `curr` is xored with every number in the `encryption` vector.

``` cpp
bool checkValidity(int num)

void extraSecurity(vector<int> &encryption)
{
    int n = encryption.size();
    for (int i = 0; i < n; ++i)
    {
        int idx = i + 2;
        if (checkValidity(idx))
        {
            encryption[i] = ~encryption[i];
        }
    }
}
```
- Now for the final change, for every number in the `encryption` vector, using its index `i + 2` is passed into the `checkValidity` function, which if returns true, that number is replaced with it's one's compliment.

- Then `writeToFile` simply saves the `encryption` vector into the [Encrypted.txt](Encrypted.txt) file.


## Decryption
### Scripts
[solve.cpp](solve.cpp)

### Explanation

- To get back the flag from the `encryption` vector, we simply have to retraced the steps from [Encrypt.cpp](Encrypt.cpp)

``` cpp
int main()
{
    fstream file;
    file.open("Encrypted.txt");
    vector<int> encryption;
    int num = 0;
    while(num!=2127757426){
        file >> num;
        encryption.push_back(num);
    }
    file.close();
    extraSecurity(encryption);
    string key = "VishwaCTF";
    applyKey(encryption, key);
    string flag = decode(encryption, key);
    cout<<flag<<'\n';
    return 0;
}
```
- So, we will first read the `encryption` vector from [Encrypted.txt](Encrypted.txt).
- Then we will apply the inverse of each function in the reverse order, i.e. `extraSecurity`, then `applyKey`, then `encode`.

``` cpp
bool checkValidity(int num)

void extraSecurity(vector<int> &encryption)
```
- The `extraSecurity` function was just applying one's complement function on some elements of the `encryption` vector on the basis of its `index`. 
- So if we apply the same `extraSecurity` function on the `encryption` vector, those numbers with the `index` that pass `checkValidity` will get flipped again using one's complement, bringing them back to their previous state.

``` cpp
void applyKey(vector<int> &encryption, string &key)
```
- Similarly, the `applyKey` function was just using each character of the `key` string to create a value `curr` and `xor` it with every number in the `encryption` vector.
- So if we apply the same `applyKey` function on the `encryption` vector, the same `curr` values will get `xored` to every number in the `encryption` vector reverting them back to their previous state.

``` cpp
int createTopping(int curr, int idx, int &not_remainder)
int createBase(int not_remainder)
int create(int curr, int idx)

string decode(vector<int> &encryption, string &key)
{
    map<pair<int,int>,int> create_result;
    for(int curr = 0; curr < 256; curr++){
        for(int idx = 2; idx < 10; idx++){
            create_result[make_pair(create(curr,idx),idx)] = curr;
        }
    }
    string decoded = "";
    for (int i = 0; i < encryption.size(); ++i)
    {
        decoded += (char)create_result[make_pair(encryption[i],i%8+2)];
    }
    return decoded;
}
```
- In the `encode` function every character as `curr` and for its index `i % 8 + 2` were passed into the `create` function and the result was put into the `encryption` vector.
- We know that the characters of the flag can only have ascii value in range `32 to 127`. So we simply bruteforce all the possibilities for `curr` from `32 to 127` and `idx` from `2 to 9` and save the results into a `map create_result`.
- Then for every number in `encryption` vector and using its index , `i % 8 + 2` as key, we get the value from the map `create_result`, which should be the character of the flag at that index, which was used as `curr`.

- Then we print the flag.

### Output

``` 
VishwaCTF{BIT5_3NCRYPT3D_D3CRYPTED_M1ND5_D33PLY_TE5T3D}
```

## Flag

The Flag is `VishwaCTF{BIT5_3NCRYPT3D_D3CRYPTED_M1ND5_D33PLY_TE5T3D}`