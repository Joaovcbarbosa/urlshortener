import java.io.*;
 
public class SDES {

	public String key1, key2, message;
    public int[][] S0 = {{ 1, 0, 3, 2},
                        {3, 2, 1, 0},
                        {0, 2, 1, 3},
                        {3, 1, 3, 2}};
    public int[][] S1 = {{ 1, 1, 2, 3},
                        {2, 0, 1, 3},
                        {3, 0, 1, 0},
                        {2, 1, 0, 3}};

    public SDES(String key, String message) {
        this.message = message;
        generateKeys(key);   
	}

    public void generateKeys(String key){   
        key = shift(P10(key));
        this.key1 = P8(key);
        this.key2 = P8(shift(shift(key)));
    }

    public String encrypt(){
        return IPReverse(F(swap(F(IP(this.message), this.key1)), this.key2));
    }

    public String decrypt(){
        return IPReverse(F(swap(F(IP(this.message), this.key2)), this.key1));
    }

    public String P10(String key){
        String permutatedKey;
        permutatedKey = (
            String.valueOf(key.charAt(2)) + 
            String.valueOf(key.charAt(4)) + 
            String.valueOf(key.charAt(1)) + 
            String.valueOf(key.charAt(6)) + 
            String.valueOf(key.charAt(3)) + 
            String.valueOf(key.charAt(9)) + 
            String.valueOf(key.charAt(0)) + 
            String.valueOf(key.charAt(8)) + 
            String.valueOf(key.charAt(7)) + 
            String.valueOf(key.charAt(5)));

        return permutatedKey;
    }

    public String shift(String key){
        String keyLeft, keyRight;
        keyLeft = shiftTable(key.substring(0, 5));
        keyRight = shiftTable(key.substring(5, 10));
        return keyLeft + keyRight;
    }

    public String shiftTable(String key){
        return (String.valueOf(key.charAt(1)) + 
                String.valueOf(key.charAt(2)) + 
                String.valueOf(key.charAt(3)) + 
                String.valueOf(key.charAt(4)) + 
                String.valueOf(key.charAt(0)));
    }

    public String P8(String key){
        String permutatedKey;
        permutatedKey = (
            String.valueOf(key.charAt(5)) + 
            String.valueOf(key.charAt(2)) + 
            String.valueOf(key.charAt(6)) + 
            String.valueOf(key.charAt(3)) + 
            String.valueOf(key.charAt(7)) + 
            String.valueOf(key.charAt(4)) + 
            String.valueOf(key.charAt(9)) + 
            String.valueOf(key.charAt(8)));

        return permutatedKey;
    }

    public String IP(String message){
        String permutatedMessage;
        permutatedMessage = (
            String.valueOf(message.charAt(1)) + 
            String.valueOf(message.charAt(5)) + 
            String.valueOf(message.charAt(2)) + 
            String.valueOf(message.charAt(0)) + 
            String.valueOf(message.charAt(3)) + 
            String.valueOf(message.charAt(7)) + 
            String.valueOf(message.charAt(4)) + 
            String.valueOf(message.charAt(6)));

        return permutatedMessage;
    }

    public String F(String message, String K){   
        String left, right, newValues;
        left = message.substring(0, 4);
        right = message.substring(4, 8);

        newValues = XOR(P4(blocks(XOR(expansion(right), K))), left); 

        return newValues + right;
    }

    public String expansion(String message){
        
        String messageExpanded;

        messageExpanded = (
            String.valueOf(message.charAt(3)) + 
            String.valueOf(message.charAt(0)) + 
            String.valueOf(message.charAt(1)) + 
            String.valueOf(message.charAt(2)) + 
            String.valueOf(message.charAt(1)) + 
            String.valueOf(message.charAt(2)) + 
            String.valueOf(message.charAt(3)) + 
            String.valueOf(message.charAt(0)));

        return messageExpanded;
    }

    public String XOR(String left, String right){
        
        int i;
        String binaryXOR = "";

        for(i = 0; i < left.length(); i++){
            if((left.charAt(i) == '1' && right.charAt(i) == '0') || (left.charAt(i) == '0' && right.charAt(i) == '1'))
                binaryXOR += '1';
            else
                binaryXOR += '0';
        }

        return binaryXOR;
    }

    public String intToBinary(int i){        
        String binary = "";
        if(i == 0) binary = "00";
        if(i == 1) binary = "01";
        if(i == 2) binary = "10";
        if(i == 3) binary = "11";

        return binary;
    }

    public String blocks(String message){
        
        String messageLeft, messageRight, S0Cell, S1Cell;  
        int S0Row, S0Column, S1Row, S1Column;   

        messageLeft = message.substring(0, 4);
        S0Row = Integer.parseInt(String.valueOf(messageLeft.charAt(0)) + String.valueOf(messageLeft.charAt(3)), 2); 
        S0Column = Integer.parseInt(String.valueOf(messageLeft.charAt(1)) + String.valueOf(messageLeft.charAt(2)), 2); 

        messageRight = message.substring(4, 8);
        S1Row = Integer.parseInt(String.valueOf(messageRight.charAt(0)) + String.valueOf(messageRight.charAt(3)), 2); 
        S1Column = Integer.parseInt(String.valueOf(messageRight.charAt(1)) + String.valueOf(messageRight.charAt(2)), 2); 


        S0Cell = intToBinary(S0[S0Row][S0Column]);
        S1Cell = intToBinary(S1[S1Row][S1Column]);
    
        return S0Cell + S1Cell;
    }

    public String P4(String message){        
        String permutatedMessage;
        permutatedMessage = (
            String.valueOf(message.charAt(1)) + 
            String.valueOf(message.charAt(3)) + 
            String.valueOf(message.charAt(2)) + 
            String.valueOf(message.charAt(0)));

        return permutatedMessage;
    }

    public String swap(String message){        
        String swappedMessage;
        swappedMessage = message.substring(4, 8) + message.substring(0, 4);

        return swappedMessage;
    }


    public String IPReverse(String message){
        String permutatedMessage;
        permutatedMessage = (
            String.valueOf(message.charAt(3)) + 
            String.valueOf(message.charAt(0)) + 
            String.valueOf(message.charAt(2)) + 
            String.valueOf(message.charAt(4)) + 
            String.valueOf(message.charAt(6)) + 
            String.valueOf(message.charAt(1)) + 
            String.valueOf(message.charAt(7)) + 
            String.valueOf(message.charAt(5)));

        return permutatedMessage;
    }

    public static void main( String args[]) throws NumberFormatException, IOException{
        int operationQuantity;  
        String operation, key, message;
        
		InputStreamReader oInputStreamReader = new InputStreamReader(System.in);
        BufferedReader oBufferedReader = new BufferedReader(oInputStreamReader);

        operationQuantity = Integer.parseInt(oBufferedReader.readLine());
        String[] respostas = new String[operationQuantity];

        for (int i = 0; i < operationQuantity; i++) {             
            operation = oBufferedReader.readLine();
            key = oBufferedReader.readLine();
            message = oBufferedReader.readLine();            
            SDES sdes = new SDES(key, message);
            if(operation.equals("C"))
                respostas[i] = sdes.encrypt();
            else
                respostas[i] = sdes.decrypt();
        }

        for (int i = 0; i < operationQuantity; i++) {           
            System.out.println(respostas[i]);
        }
    }
}
