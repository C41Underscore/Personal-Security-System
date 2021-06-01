package src;

import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;
import java.util.concurrent.*;
import java.net.NetworkInterface;


class Main {
    public static void main(String[] args) {
        ServerSocket s = null;
        ExecutorService ex = null;
        System.out.println("Starting server...");
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
                ex.submit(new CameraProtocol(s.accept()));
            } catch(IOException e)
            {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}