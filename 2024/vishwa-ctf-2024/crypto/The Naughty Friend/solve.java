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
