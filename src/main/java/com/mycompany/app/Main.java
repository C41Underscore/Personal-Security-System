package com.mycompany.app;

import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.*;
import java.net.NetworkInterface;

// TODO: Camera Code
// TODO: Google Drive interface
// TODO: Logging
// TODO: Camera interface/ getting images
// TODO: Email interface


class Main {
    public static void main(String[] args) {
        System.out.println("Starting server...");
        ServerSocket s = null;
        ExecutorService ex = null;
        NetworkScanner ns = new NetworkScanner("./mac_to_ip_converter.py", "3e:f9:ff:03:7b:fe");
        GoogleDriveInterface gdi = new GoogleDriveInterface(System.getProperty("user.home") + "/security-system/tmp/");
        Timer t = new Timer();
        t.schedule(new TimerTask() {
            @Override
            public void run() {
                try
                {
                    ns.scan();
                }
                catch (IOException | InterruptedException e)
                {
                    System.out.println(e.getMessage());
                }
            }
        }, 0, 20000);
        t.schedule(new TimerTask() {
            @Override
            public void run() {
                gdi.reduceQueue();
            }
        }, 0, 10000);
        try
        {
            s = new ServerSocket(8080);
        } catch(IOException e)
        {
            System.out.println("Error: " + e.getMessage());
            System.exit(-1);
        }
        ex = Executors.newFixedThreadPool(6);
        while(true)
        {
            try
            {
                ex.submit(new CameraProtocol(s.accept(), ns, gdi));
            } catch(IOException e)
            {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}