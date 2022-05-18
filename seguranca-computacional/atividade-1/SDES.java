import java.io.*;
import java.util.*;
 
public class SDES {

	public String K1, K2;

    public SDES(String K) {
        K1 = generateK1(K);
        K2 = generateK2(K);
        System.out.println(K1);
        System.out.println(K2);
	}

    public String generateK1(String K){
        String K1, K1Left, K1Right;
        K1 = P10(K);
        K1Left = K1.substring(0, 5);
        K1Left = rotation(K1Left);
        K1Right = K1.substring(5, 10);
        K1Right = rotation(K1Right);
        K1 = P8(K1Left + K1Right);
        return K1;
    }

    public String generateK2(String K){
        String K2, K2Left, K2Right;
        K2 = P10(K);
        K2Left = K2.substring(0, 5);
        K2Left = rotation(K2Left);
        K2Left = rotation(K2Left);
        K2Left = rotation(K2Left);
        K2Right = K2.substring(5, 10);
        K2Right = rotation(K2Right);
        K2Right = rotation(K2Right);
        K2Right = rotation(K2Right);
        K2 = P8(K2Left + K2Right);
        return K2;
    }

    public String P10(String K){
        String KPermutated;
        KPermutated = (
            String.valueOf(K.charAt(2)) + 
            String.valueOf(K.charAt(4)) + 
            String.valueOf(K.charAt(1)) + 
            String.valueOf(K.charAt(6)) + 
            String.valueOf(K.charAt(3)) + 
            String.valueOf(K.charAt(9)) + 
            String.valueOf(K.charAt(0)) + 
            String.valueOf(K.charAt(8)) + 
            String.valueOf(K.charAt(7)) + 
            String.valueOf(K.charAt(5)));

        return KPermutated;
    }

    public String P8(String K){
        String KPermutated;
        KPermutated = (
            String.valueOf(K.charAt(5)) + 
            String.valueOf(K.charAt(2)) + 
            String.valueOf(K.charAt(6)) + 
            String.valueOf(K.charAt(3)) + 
            String.valueOf(K.charAt(7)) + 
            String.valueOf(K.charAt(4)) + 
            String.valueOf(K.charAt(9)) + 
            String.valueOf(K.charAt(8)));

        return KPermutated;
    }

    public String rotation(String K){
        String KRotated;
        KRotated = (
            String.valueOf(K.charAt(1)) + 
            String.valueOf(K.charAt(2)) + 
            String.valueOf(K.charAt(3)) + 
            String.valueOf(K.charAt(4)) + 
            String.valueOf(K.charAt(0)));

        return KRotated;
    }

    public static void main( String args[]) throws NumberFormatException, IOException{
        int L;  
        String O, K, B;
        
		InputStreamReader oInputStreamReader = new InputStreamReader(System.in);
        BufferedReader oBufferedReader = new BufferedReader(oInputStreamReader);

        L = Integer.parseInt(oBufferedReader.readLine());
        for (int i = 0; i < L; i++) {             
            O = oBufferedReader.readLine();
            K = oBufferedReader.readLine();
            B = oBufferedReader.readLine();            
            SDES sdes = new SDES(K);
        }
    }
}
