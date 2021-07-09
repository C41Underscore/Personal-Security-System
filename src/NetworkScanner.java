package src;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;

public class NetworkScanner
{
    private final String cmd = "nmap -sn 192.168.0.0/24";
    private String pathToMACConverter;
    private ArrayList<String> requiredAddresses;
    private Boolean status = false;

    public NetworkScanner(String pathToMACConverter, String...requiredAddresses)
    {
        this.pathToMACConverter = pathToMACConverter;
        this.requiredAddresses = new ArrayList<String>();
        this.requiredAddresses.addAll(Arrays.asList(requiredAddresses));
        this.generateConverter();
    }

    public Boolean requiredAddressPresent()
    {
        return this.status;
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
    public void scan() throws InterruptedException, IOException {
        System.out.println("Scanning network...");
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
        // Search for required addresses in found addresses
        ArrayList<String> foundAddresses = new ArrayList<String>();
        while((line = buf.readLine()) != null)
        {
            foundAddresses.add(line);
        }
        for(int i = 0; i < this.requiredAddresses.size(); i++)
        {
            for(int j = 0; j < foundAddresses.size(); j++)
            {
                System.out.println(foundAddresses.get(j));
                if(this.requiredAddresses.get(i).compareTo(foundAddresses.get(j)) == 0)
                {
                    // If an address is found, swap it with the first, return true
                    String temp = this.requiredAddresses.get(0);
                    String foundAddress = this.requiredAddresses.get(i);
                    this.requiredAddresses.remove(i);
                    if(this.requiredAddresses.size() > 0)
                    {
                        this.requiredAddresses.add(0, foundAddress);
                    }
                    else
                    {
                        this.requiredAddresses.add(foundAddress);
                    }
                    this.requiredAddresses.add(i, temp);
                    this.status = true;
                    return;
                }
            }
        }
        // If no addresses are found, return false
        this.status = false;
    }
}
