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

    public CameraProtocol(Socket cameraSocket)
    {
        this.cameraSocket = cameraSocket;
        try
        {
            InetAddress ip = InetAddress.getLocalHost();
            NetworkInterface network = NetworkInterface.getByInetAddress(ip);
            byte[] mac = network.getHardwareAddress();
            StringBuilder bobTheBuilder = new StringBuilder();
            for(int i = 0; i < mac.length; i++)
            {
                bobTheBuilder.append(String.format(
                        "%02X%s", mac[i],
                        (i < mac.length - 1) ? "-" : ""));
            }
            System.out.println(bobTheBuilder.toString());
        } catch(SocketException | UnknownHostException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
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
            Thread.sleep(1000);
            while((receivedFromCamera = in.readLine()) != null)
            {
                System.out.println(receivedFromCamera);
            }
            this.in.close();
            this.out.close();
        } catch(IOException | InterruptedException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
