package com.mycompany.app;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.MalformedURLException;
import java.net.Socket;
import java.net.URL;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;


public class CameraProtocol extends Thread {
    private URL source = null;
    private Socket cameraSocket = null;
    private BufferedReader in = null;
    private PrintWriter out = null;
    private NetworkScanner ns = null;
    private GoogleDriveInterface gdi = null;

    public CameraProtocol(Socket cameraSocket, NetworkScanner ns, GoogleDriveInterface gdi)
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
        this.gdi = gdi;
    }

    public void run()
    {
        DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");
        LocalDateTime ldt = null;
        char[] receivedFromCamera = new char[512];
        try
        {
            Thread.sleep(500);
            while(in.read(receivedFromCamera, 0, 512) != -1)
            {
                String charData = new String(receivedFromCamera);
                if(charData.contains("1"))
                {
                    synchronized (ns)
                    {
                        if(!ns.requiredAddressPresent())
                        {
                            // Replace this with HTTP request to camera
                            BufferedImage image = ImageIO.read(this.source);
                            System.out.println("Image acquired from " + this.source);
                            // Handle image
                            StringBuilder imageFilepath = new StringBuilder();
                            ldt = LocalDateTime.now();
                            String fileDateAndTime = ldt.format(dateFormatter);
                            String absoluteFilepath = this.gdi.getImageQueuePath() + fileDateAndTime;
                            if(!new File(absoluteFilepath).exists())
                            {
                                new File(absoluteFilepath).mkdirs();
                            }
                            imageFilepath.append(fileDateAndTime).append("/").append(ldt.format(timeFormatter));
                            ImageIO.write(image, "jpg", new File(this.gdi.getImageQueuePath() + imageFilepath.toString()));
                            // Place it into queue to be uploaded to google drive
                            synchronized (this.gdi)
                            {
                                this.gdi.queueImage(imageFilepath.toString());
                            }
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
