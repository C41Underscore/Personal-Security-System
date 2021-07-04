package src;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;

public class NetworkScanner
{
    private final String cmd = "nmap -sn 192.168.0.0/24";
    private String pathToMACConverter;
    private ArrayList<String> requiredAddresses;

    public static void main(String[] args) throws IOException, InterruptedException {
        NetworkScanner ns = new NetworkScanner("src/convert_ip_to_mac.py");
        ns.scan();
    }

    public NetworkScanner(String pathToMACConverter, String...requiredAddresses)
    {
        this.pathToMACConverter = pathToMACConverter;
        this.requiredAddresses = new ArrayList<String>();
        this.requiredAddresses.addAll(Arrays.asList(requiredAddresses));
        this.generateConverter();
    }

    // create the python3 script to convert ip addresses to MAC addresses
    private void generateConverter()
    {
        try
        {
            FileWriter fw = new FileWriter(pathToMACConverter);
            fw.write("from arpreq import arpreq\n");
            fw.write("from sys import argv\n");
            fw.write("for i in range(1, len(argv)):\n");
            fw.write("  print(arpreq(argv[i]))\n");
            fw.close();
        }
        catch (IOException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }

    // returns true if a specified MAC address is present on the subnetwork
    // returns false if no specified MAC addresses are on the subnetwork
    public Boolean scan() throws InterruptedException, IOException {
        Process pr = Runtime.getRuntime().exec(this.cmd);
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
                        .replaceAll("\\(", "")
                        .replaceAll("\\)", "");
                addresses.add(line);
            }
        }
        addresses.remove(addresses.size()-1);
        StringBuilder cmdPython = new StringBuilder();
        cmdPython.append("python3 ").append(this.pathToMACConverter);
        for(String address : addresses)
        {
            cmdPython.append(" ").append(address);
        }
        pr = Runtime.getRuntime().exec(cmdPython.toString());
        pr.waitFor();
        buf = new BufferedReader((new InputStreamReader(pr.getInputStream())));
        while((line = buf.readLine()) != null)
        {
            System.out.println(line);
        }
        return false;
    }
}
