package src;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.*;
import java.util.Arrays;


public class CameraProtocol extends Thread {
    private String URL = null;
    private Socket cameraSocket = null;
    private BufferedReader in = null;
    private PrintWriter out = null;
    private NetworkScanner ns = null;

    public CameraProtocol(Socket cameraSocket, NetworkScanner ns)
    {
        this.cameraSocket = cameraSocket;
        try
        {
            this.in = new BufferedReader(new InputStreamReader(this.cameraSocket.getInputStream()));
            this.out = new PrintWriter(this.cameraSocket.getOutputStream(), true);
        } catch(IOException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
        StringBuilder bobTheBuilder = new StringBuilder();
        bobTheBuilder.append("http:/");
        bobTheBuilder.append(cameraSocket.getInetAddress().toString());
        bobTheBuilder.append("/cam-hi.jpg");
        this.URL = bobTheBuilder.toString();
        System.out.println("New camera connected: " + this.URL);
        this.ns = ns;
    }

    public void run()
    {
        String receivedFromCamera = "";
        try
        {
            Thread.sleep(1000);
            while((receivedFromCamera = in.readLine()) != null)
            {
                if(receivedFromCamera.contains("1"))
                {
                    synchronized (ns)
                    {
                        if(!ns.requiredAddressPresent())
                        {
                            System.out.println("Take picture! - " + this.URL);
                        }
                    }

                }
            }
            this.in.close();
            this.out.close();
            this.cameraSocket.close();
        } catch(IOException | InterruptedException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
