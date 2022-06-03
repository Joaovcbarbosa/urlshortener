import java.io.*;
 
public class RC4 {
    public byte[] S = new byte[256];
    public byte[] T = new byte[256];
    public byte[] key = new byte[256];
 
    public RC4(byte[] key) {  
        this.key = key;
        SInitialization();
        SPermutation();
    }
 
    public void SInitialization(){
        int i;
 
        for (i = 0; i < 256; i++) {
            S[i] = (byte) i;
            T[i] = key[i % key.length];
        }
    }
 
    public void SPermutation(){
        int i, j;    
 
        j = 0;
        for (i = 0; i < 256; i++) {
            j = (j + S[i] + T[i]) & 0xFF;
            swap(i, j);
        }
    }
 
    public byte[] encrypt(byte[] plainText) {
        int i = 0, j = 0, k, t;
        byte[] encryptedTextBytes = new byte[plainText.length];
 
        for (k = 0; k < plainText.length; k++) {
            i = (i + 1) & 0xFF;
            j = (j + S[i]) & 0xFF;
            swap(i, j);
            t = (S[i] + S[j]) & 0xFF;
            encryptedTextBytes[k] = (byte) (plainText[k] ^ S[t]);
        }
        return encryptedTextBytes;
    }
 
    public void swap(int i, int j){        
        byte aux;
 
        aux = S[j];
        S[j] = S[i];
        S[i] = aux;
    }
 
    public String byteToHexadecimal(byte[] bytes){
        StringBuilder oStringBuilder = new StringBuilder();
 
        for (byte b : bytes) {
            oStringBuilder.append(String.format("%X:", b));
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