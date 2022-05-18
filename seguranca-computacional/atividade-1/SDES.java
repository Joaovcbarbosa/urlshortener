import java.io.*;
 
public class SDES {

	public String K1, K2, B;
    public int[][] S0 = {{ 1, 0, 3, 2},
                        {3, 2, 1, 0},
                        {0, 2, 1, 3},
                        {3, 1, 3, 2}};
    public int[][] S1 = {{ 1, 1, 2, 3},
                        {2, 0, 1, 3},
                        {3, 0, 1, 0},
                        {2, 1, 0, 3}};

    public SDES(String K, String B) {
        this.B = B;
        generateKeys(K);   
	}

    public void generateKeys(String K){   
        K = shift(P10(K));
        this.K1 = P8(K);
        this.K2 = P8(shift(shift(K)));
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

    public String shift(String K){
        String KLeft, KRight;
        KLeft = shiftTable(K.substring(0, 5));
        KRight = shiftTable(K.substring(5, 10));
        return KLeft + KRight;
    }

    public String shiftTable(String K){
        return (String.valueOf(K.charAt(1)) + 
                String.valueOf(K.charAt(2)) + 
                String.valueOf(K.charAt(3)) + 
                String.valueOf(K.charAt(4)) + 
                String.valueOf(K.charAt(0)));
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

    public String encrypt(){
        return IPReverse(F(swap(F(IP(B), this.K1)), this.K2));
    }

    public String decrypt(){
        return IPReverse(F(swap(F(IP(B), this.K2)), this.K1));
    }

    public String IP(String B){
        String BPermutated;
        BPermutated = (
            String.valueOf(B.charAt(1)) + 
            String.valueOf(B.charAt(5)) + 
            String.valueOf(B.charAt(2)) + 
            String.valueOf(B.charAt(0)) + 
            String.valueOf(B.charAt(3)) + 
            String.valueOf(B.charAt(7)) + 
            String.valueOf(B.charAt(4)) + 
            String.valueOf(B.charAt(6)));

        return BPermutated;
    }

    public String F(String B, String K){   
        String BLeft, BRight, L;
        L = B.substring(0, 4);

        if(K == K1) BLeft = B.substring(0, 4);
        else BLeft = B.substring(4, 8);

        BRight = B.substring(4, 8);

        BRight = expansion(BRight);
        BRight = XOR(BRight, K); 
        BRight = Blocks(BRight); 
        BRight = P4(BRight); 
        BRight = XOR(BRight, L); 

        return BRight + BLeft;
    }

    public String expansion(String B){
        
        String BExpanded;

        BExpanded = (
            String.valueOf(B.charAt(3)) + 
            String.valueOf(B.charAt(0)) + 
            String.valueOf(B.charAt(1)) + 
            String.valueOf(B.charAt(2)) + 
            String.valueOf(B.charAt(1)) + 
            String.valueOf(B.charAt(2)) + 
            String.valueOf(B.charAt(3)) + 
            String.valueOf(B.charAt(0)));

        return BExpanded;
    }

    public String XOR(String Left, String Right){
        
        int i;
        String BXOR = "";

        for(i = 0; i < Left.length(); i++){
            if((Left.charAt(i) == '1' && Right.charAt(i) == '0') || (Left.charAt(i) == '0' && Right.charAt(i) == '1'))
                BXOR += '1';
            else
                BXOR += '0';
        }

        return BXOR;
    }
    public String intToBinary(int i){        
        String binary = "";
        if(i == 0) binary = "00";
        if(i == 1) binary = "01";
        if(i == 2) binary = "10";
        if(i == 3) binary = "11";

        return binary;
    }

    public String Blocks(String B){
        
        String BLeft, BRight, S0Cell, S1Cell;  
        int S0Row, S0Column, S1Row, S1Column;   

        BLeft = B.substring(0, 4);
        S0Row = Integer.parseInt(String.valueOf(BLeft.charAt(0)) + String.valueOf(BLeft.charAt(3)), 2); 
        S0Column = Integer.parseInt(String.valueOf(BLeft.charAt(1)) + String.valueOf(BLeft.charAt(2)), 2); 

        BRight = B.substring(4, 8);
        S1Row = Integer.parseInt(String.valueOf(BRight.charAt(0)) + String.valueOf(BRight.charAt(3)), 2); 
        S1Column = Integer.parseInt(String.valueOf(BRight.charAt(1)) + String.valueOf(BRight.charAt(2)), 2); 


        S0Cell = intToBinary(S0[S0Row][S0Column]);
        S1Cell = intToBinary(S1[S1Row][S1Column]);
    
        return S0Cell + S1Cell;
    }

    public String P4(String B){        
        String BPermutated;
        BPermutated = (
            String.valueOf(B.charAt(1)) + 
            String.valueOf(B.charAt(3)) + 
            String.valueOf(B.charAt(2)) + 
            String.valueOf(B.charAt(0)));

        return BPermutated;
    }

    public String swap(String B){        
        String BSwaped;
        BSwaped = B.substring(4, 8) + B.substring(0, 4);

        return BSwaped;
    }


    public String IPReverse(String B){
        String BPermutated;
        BPermutated = (
            String.valueOf(B.charAt(3)) + 
            String.valueOf(B.charAt(0)) + 
            String.valueOf(B.charAt(2)) + 
            String.valueOf(B.charAt(4)) + 
            String.valueOf(B.charAt(6)) + 
            String.valueOf(B.charAt(1)) + 
            String.valueOf(B.charAt(7)) + 
            String.valueOf(B.charAt(5)));

        return BPermutated;
    }

    public static void main( String args[]) throws NumberFormatException, IOException{
        int L;  
        String O, K, B;
        
		InputStreamReader oInputStreamReader = new InputStreamReader(System.in);
        BufferedReader oBufferedReader = new BufferedReader(oInputStreamReader);

        L = Integer.parseInt(oBufferedReader.readLine());
        String[] respostas = new String[L];

        for (int i = 0; i < L; i++) {             
            O = oBufferedReader.readLine();
            K = oBufferedReader.readLine();
            B = oBufferedReader.readLine();            
            SDES sdes = new SDES(K, B);
            if(O.equals("C"))
                respostas[i] = sdes.encrypt();
            else
                respostas[i] = sdes.decrypt();
        }

        for (int i = 0; i < L; i++) {           
            System.out.println(respostas[i]);
        }
    }
}
