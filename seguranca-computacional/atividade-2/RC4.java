import java.io.*;

public class RC4 {
    private byte[] S = new byte[256];
    private byte[] T = new byte[256];

    public RC4(byte[] key) {        
        int i, j;
        byte tmp;
        for (i = 0; i < 256; i++) {
            S[i] = (byte) i;
            T[i] = key[i % key.length];
        }
        j = 0;
        for (i = 0; i < 256; i++) {
            j = (j + S[i] + T[i]) & 0xFF;
            tmp = S[j];
            S[j] = S[i];
            S[i] = tmp;
        }
    }

    public byte[] encrypt(byte[] plaintext) {
        byte[] ciphertext = new byte[plaintext.length];
        int i = 0, j = 0, k, t;
        byte tmp;
        for (int counter = 0; counter < plaintext.length; counter++) {
            i = (i + 1) & 0xFF;
            j = (j + S[i]) & 0xFF;
            tmp = S[j];
            S[j] = S[i];
            S[i] = tmp;
            t = (S[i] + S[j]) & 0xFF;
            k = S[t];
            ciphertext[counter] = (byte) (plaintext[counter] ^ k);
        }
        return ciphertext;
    }

    public String byteToHexadecimal(byte[] bytes){
        StringBuilder oStringBuilder = new StringBuilder();
        for (byte b : bytes) {
            oStringBuilder.append(String.format("%02X:", b));
        }
        return oStringBuilder.toString().toLowerCase();        
    }
    
    public static void main(String args[]) throws Exception {
        InputStreamReader oInputStreamReader = new InputStreamReader(System.in);
        BufferedReader oBufferedReader = new BufferedReader(oInputStreamReader);
        String plainText, key, encryptedTextHexadecimal;
        
        plainText = oBufferedReader.readLine();
        key = oBufferedReader.readLine();

        RC4 RC4 = new RC4(key.getBytes()); 
        byte[] encryptedTextBytes = RC4.encrypt(plainText.getBytes());

        encryptedTextHexadecimal = RC4.byteToHexadecimal(encryptedTextBytes);
        System.out.println(encryptedTextHexadecimal);    
    }
}