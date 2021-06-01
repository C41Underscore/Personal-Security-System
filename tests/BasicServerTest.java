package tests;

import java.util.ArrayList;
import java.io.IOException;
import java.net.Socket;

class BasicServerTest {
    public static void main(String[] args) {
        ArrayList<Socket> testSockets = new ArrayList<Socket>();
        for(int i = 0; i < 6; i++)
        {
            try
            {
                testSockets.add(new Socket("localhost", 8080));
            }
            catch(IOException e)
            {
                System.out.println("Error: " + e.getMessage());
            }
        }
        System.out.println(testSockets.size());
        for(int i = 0; i < 6; i++)
        {
            try
            {
                testSockets.get(i).close();
            }
            catch(IOException e)
            {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }   
}
