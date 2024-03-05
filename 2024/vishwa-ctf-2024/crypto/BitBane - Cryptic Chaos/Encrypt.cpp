#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

int createTopping(int curr, int idx, int &not_remainder)
{
    int temp = 0;
    int num = 1;
    num = num << 1;
    while (curr)
    {
        int remainder = curr % idx;
        if (remainder)
        {
            temp = temp * 10 + remainder;
            curr = curr - remainder;
        }
        else
        {
            num = num | 1;
            curr = curr / idx;
        }
        num = num << 1;
    }
    temp = temp << 1;
    temp = temp | 1;
    not_remainder = temp;
    return num | 1;
}

int createBase(int not_remainder)
{
    int num = 0;
    for (int i = 0; i < 30; ++i)
    {
        if (not_remainder)
        {
            num = num | (not_remainder & 1);
            not_remainder = not_remainder >> 1;
        }
        num = num << 1;
    }
    return num;
}

int create(int curr, int idx)
{
    int not_remainder = 0;
    int topping = createTopping(curr, idx, not_remainder);
    int base = createBase(not_remainder);
    int num = base | topping;
    return num;
}

bool checkValidity(int num)
{
    for (int i = 2; i * i < num; ++i)
    {
        if (num % i == 0)
            return false;
    }
    return true;
}

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

void writeToFile(const vector<int> &encryption)
{
    ofstream outfile("Encrypted.txt");
    string data;
    for (auto ele : encryption)
    {
        data += to_string(ele);
        data += " ";
    }
    outfile << data;
    outfile.close();
}

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