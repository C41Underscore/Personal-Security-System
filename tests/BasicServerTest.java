package tests;

import java.util.ArrayList;
import java.io.IOException;
import java.net.Socket;
import java.io.PrintWriter;
import java.io.BufferedReader;
import java.io.InputStreamReader;

class BasicServerTest {
    public static void main(String[] args) {
        ArrayList<Socket> testSockets = new ArrayList<Socket>();
        ArrayList<PrintWriter> outs = new ArrayList<PrintWriter>();
        ArrayList<BufferedReader> ins = new ArrayList<BufferedReader>();
        for(int i = 0; i < 6; i++)
        {
            try
            {
                testSockets.add(new Socket("localhost", 8080));
                outs.add(new PrintWriter(testSockets.get(i).getOutputStream()));
                ins.add(new BufferedReader(new InputStreamReader(testSockets.get(i).getInputStream())));
            }
            catch(IOException e)
            {
                System.out.println("Error: " + e.getMessage());
            }
        }
        for(int i = 0; i < 6; i++)
        {
            outs.get(i).print("Hello from test ");
            outs.get(i).println(i);
            outs.get(i).flush();
        }
        for(int i = 0; i < 6; i++)
        {
            try
            {
                testSockets.get(i).close();
                ins.get(i).close();
                outs.get(i).close();
            }
            catch(IOException e)
            {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }   
}
