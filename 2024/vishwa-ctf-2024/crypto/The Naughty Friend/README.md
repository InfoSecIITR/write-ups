# The Naughty Friend
## Author : Kanishk Kumar

## Source

- One of my friends Dhruv is a cryptography genius, but he likes to annoy me by playing pranks with my passwords. He recently changed my accounts password and has given the following files as hints, he also gave this buggy code which had some import statements removed, help me retrieve my lost password!!!

### Files:
- [Code.txt](Code.txt)
- [Encryption&Key.txt](Encryption&Key.txt)

## Encryption

- First step would be to fix the code given in [Code.txt](Code.txt)
    - Just had to import the `java.security` module and add the `catch Exception` part.

- The Fixed Code is at [Fixed_Code.java](Fixed_Code.java)

- The Code is for encryption using `Blowfish` which is a `Symmetric Cipher` that replaced `DES`.
- It's applying the same `cipher` obtained from the same `secretKey` and `ivbytes` twice on the `plaintext`.

- Analysing the [Encryption&Key.txt](Encryption&Key.txt) file, the given `Key` cannot be the key to Blowfish Encryption as its `length` is more that what Blowfish accepts as Key, which is `4 to 56 bytes`, and the Encryption is the ciphertext in base64 format

## Decryption
### Scripts
- [solve.java](solve.java)
- [xor59.py](xor59.py)

### Explanation

- Looking closely at the `Key` since it wasn't the key to decrypt the Blowfish Encryption, I searched it for Cipher Indentification and it turned out to be `Rot-47`, which on deciphering read -
```
YEK EHT FO STRAP "tnatropmI tsoM eht era dnE dna gninnigeB ehT"
```
- Which on reversing read -
```
"The Beginning and End are the Most Important" PARTS OF THE KEY
```

- After a lot of guesses and help from admin I reached to the point that the Key is the concatenation of first and last letters of each word in the quoted string : `TeBgadEdaeteMtIt`

- So I took the `base64 encoded ciphertext` and the `Key` and tried to apply `double Blowfish decryption` on them as provided in the Code, which didn't work
- As the `IV` was generated randomly in the Code provided and there was no way to get its value, I simply changed the mode of encryption from `CBC to ECB` and got rid of the `IV`, in hopes that I will xor the rest of the data later if the first block comes back right.
- It gave me the entire decrypted data in `ECB Mode`. So, I guess that was also something to fix in the broken code.
```java
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Scanner;

public class solve {
    public static void main(String[] args) throws Exception {
        String ciphertext = "mF1b8dUwdPVhc/0Hfu1ONep6V6oTHnRqhEMEgtCsge+GncFq9YbX1eCkYwmrHTvajsiyj/vd4IV0BbZI1Obq3/uD7nDyAJ/FxZJNAFRAUuGm3LLXf4vn3zKWsZATypBkkgEQLWfIpg0tP13wJRhk6JUVPi17AaKHrodTtWOq54FqKIaT1DoifMjtJ4TCG3IXmjEo+6ZsBokIjxeCjamGBwNAqFaqIikkHJo7L1PiCFds/lAaB38KqHGL/E2pfw0CK3XYzKV8gBdwhnrUq1UN1Q";
        byte[] ct = Base64.getDecoder().decode(ciphertext);
        String keyString = "TeBgadEdaeteMtIt";
        byte[] keyData = keyString.getBytes();
        SecretKey secretKey = new SecretKeySpec(keyData, "Blowfish");
        String plaintext = encrypt(ct, secretKey);
        System.out.println("Encrypted Text: " + plaintext);
    }

    private static String encrypt(byte[] ct, SecretKey secretKey) throws Exception {
        Cipher cipher = Cipher.getInstance("Blowfish/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] decryptedBytes = cipher.doFinal(ct);
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] plaintext = cipher.doFinal(decryptedBytes);
        return new String(plaintext);
    }
}
```

- The `plaintext` output said that there is another stage, and they are using `Xerox-Of-Rat` Encryption with Key between `0 to 100` and the message starts with `Vml` - Standard XOR

### Output

```
Encrypted Text: This is the final hint, the answer to this encrption starts with: Vml and the key lies btween 0 to 100 , Xerox-Of-Rat Encrption : b'mVWAZs_Sj\ni|^\nyzX\x08u\x08vsq~c\nqWulmnali]qsmQb\tmAaUnCvcW\x02'
```

### Xor Decryption

- The Explanation says that the answer starts with `Vml`, so the `XorKey` will be `ascii value of 'm' ^ ascii value of 'V'`
- Then we simply apply the Xor Key to the entire string.

```py
ct = b'mVWAZs_Sj\ni|^\nyzX\x08u\x08vsq~c\nqWulmnali]qsmQb\tmAaUnCvcW\x02'
key = 59
pt = b''.join([(byte ^ key).to_bytes(1,'big') for byte in ct])
print(pt)
```

- The resulting `pt` seemed like a `base64` encoded data so we decoded it to get the `flag`.

```py
import base64
flag = base64.b64decode(pt)
print(flag.decode())
```

### Output
```
b'VmlzaHdhQ1RGe1BAc3N3MHJEX1JlNWVUZWRfJHVjY2VzZnUxMXl9'
VishwaCTF{P@ssw0rD_Re5eTed_$uccesfu11y}
```

## Flag

The Flag is `VishwaCTF{P@ssw0rD_Re5eTed_$uccesfu11y}`