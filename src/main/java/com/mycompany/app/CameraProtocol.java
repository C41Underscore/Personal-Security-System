package com.mycompany.app;

import javax.imageio.ImageIO;
import java.awt.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.MalformedURLException;
import java.net.Socket;
import java.net.URL;


public class CameraProtocol extends Thread {
    private URL source = null;
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
        try
        {
            this.source = new URL(bobTheBuilder.toString());
        } catch(MalformedURLException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
        System.out.println("New camera connected: " + this.source);
        this.ns = ns;
    }

    public void run()
    {
        String receivedFromCamera = "";
        try
        {
            Thread.sleep(500);
            while((receivedFromCamera = in.readLine()) != null)
            {
                if(receivedFromCamera.contains("1"))
                {
                    synchronized (ns)
                    {
                        if(!ns.requiredAddressPresent())
                        {
                            // Replace this with HTTP request to camera
                            Image image = ImageIO.read(this.source);
                            System.out.println("Image acquired: " + image);
                            // Handle image
                            // Place it into queue to be uploaded to google drive
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
