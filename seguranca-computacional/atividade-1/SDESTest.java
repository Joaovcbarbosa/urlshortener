
 import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.*;
 
public class SDESTest {

    SDES sdes = new SDES("1000000000", "10101010");

    @Test
    public void K1Test(){
        sdes.generateKeys("1010000010");
        assertEquals("10100100", sdes.K1);
        sdes.generateKeys("1000000000");
        assertEquals("10000000", sdes.K1);
    }

    @Test
    public void K2Test(){
        sdes.generateKeys("1010000010");
        assertEquals("01000011", sdes.K2);
        sdes.generateKeys("1000000000");
        assertEquals("00000001", sdes.K2);
    }

    @Test
    public void IPTest(){
        assertEquals("11001100", sdes.IP("01010101"));
    }

    @Test
    public void FTest(){
        sdes.K1 = "10000000";
        sdes.K2 = "00000001";
        assertEquals("01111100", sdes.F("11001100", "10000000"));
        assertEquals("00100111", sdes.F("11000111", "00000001"));
    }

    @Test
    public void expansionTest(){
        assertEquals("10101010", sdes.expansion("0101"));
    }

    @Test
    public void XORTest(){
        assertEquals("00101011", sdes.XOR("10101010", "10000001"));
    }
	
    @Test
    public void BlocksTest(){
        assertEquals("0001", sdes.Blocks("00101011"));
    }

    @Test
    public void P4Test(){
        assertEquals("0100", sdes.P4("0001"));
    }
	
    @Test
    public void swap(){
        assertEquals("11000111", sdes.swap("01111100"));
    }

}
