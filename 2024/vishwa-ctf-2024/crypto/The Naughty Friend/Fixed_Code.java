import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;
import java.util.Base64;
import java.util.Scanner;

public class Fixed_Code {
    public static void main(String[] args) {
        Scanner myObj = new Scanner(System.in);
        System.out.println("Enter the text to be encrypted: ");
        String plaintext = myObj.nextLine();
        System.out.println("Enter the key: ");
        String keyString = myObj.nextLine();
        myObj.close();
        try {
            byte[] keyData = keyString.getBytes();
            SecretKey secretKey = new SecretKeySpec(keyData, "Blowfish");
            String encryptedText = encrypt(plaintext, secretKey);
            System.out.println("Encrypted Text: " + encryptedText);
        } catch (Exception e) {
            System.out.println("Encryption failed: " + e.getMessage());
        }
    }
    
    private static String encrypt(String plaintext, SecretKey secretKey) throws Exception {
        Cipher cipher = Cipher.getInstance("Blowfish/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] encryptedBytes = cipher.doFinal(plaintext.getBytes());
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        encryptedBytes = cipher.doFinal(plaintext.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }
}
