package src;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.util.Arrays;
import java.net.Socket;

public class CameraProtocol extends Thread {
    private String URL = null;
    private Socket cameraSocket = null;
    private BufferedReader in = null;
    private PrintWriter out = null;

    public CameraProtocol(Socket cameraSocket)
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
    }

    public void run()
    {
        String receivedFromCamera = "";
        try
        {
            while((receivedFromCamera = in.readLine()) != null)
            {
                System.out.println(receivedFromCamera);
            }
            this.in.close();
            this.out.close();
        } catch(IOException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
