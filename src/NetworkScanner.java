package src;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;

public class NetworkScanner
{
    public static void main(String[] args) throws IOException, InterruptedException {
        String cmd = "nmap -sn 192.168.0.0/24";
        Runtime run = Runtime.getRuntime();
        Process pr = run.exec(cmd);
        pr.waitFor();
        BufferedReader buf = new BufferedReader((new InputStreamReader(pr.getInputStream())));
        String line = "";
        ArrayList<String> addresses = new ArrayList<String>();
        int count = 0;
        while((line = buf.readLine()) != null)
        {
            if(++count % 2 == 0)
            {
                line = line.substring(line.length() - 13);
                line = line.stripLeading()
                        .replaceAll("\\(", " ")
                        .replaceAll("\\)", "");
                addresses.add(line);
            }
        }
        addresses.remove(addresses.size()-1);
        StringBuilder cmdPython = new StringBuilder();
        cmdPython.append("python3 src/convert_ip_to_mac.py");
        for(String address : addresses)
        {
            cmdPython.append(" ");
            cmdPython.append(address);
        }
        System.out.println(cmdPython.toString());
        pr = Runtime.getRuntime().exec(cmdPython.toString());
        pr.waitFor();
        buf = new BufferedReader((new InputStreamReader(pr.getInputStream())));
        while((line = buf.readLine()) != null)
        {
            System.out.println(line);
        }
    }
}
