import java.util.*;  
import java.io.*;

public class SDES {
    public static void main( String args[]){
        String L, O, K, B;  
        
        DataInputStream inp=new DataInputStream(System.in);
        L = sc.nextLine();
        for (int i = 0; i < Integer.parseInt(L); i++) {             
            O = sc.nextLine();     
            K = sc.nextLine();    
            B = sc.nextLine();  
            System.out.println("O: " + O + "K: " +K +" B: " + B);
        }
    }
}
