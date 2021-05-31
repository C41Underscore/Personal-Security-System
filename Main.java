import java.net.Socket;
import java.io.IOException;

class Main {
    public static void main(String[] args) {
        System.out.println("Hello there!");
        Socket s = new Socket();
        try {
            s.close();
        } catch (IOException e) {
            System.out.println("Wow!");
        }
    }
}