import java.io.*;
import java.util.*;
 
public class SDES {
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
            System.out.println("O: " + O + " K: " +K +" B: " + B);
        }
    }
}
