package com.mycompany.app;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.FileContent;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.client.util.DateTime;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.services.drive.Drive;
import com.google.api.services.drive.DriveScopes;
import com.google.api.services.drive.model.File;
import com.google.api.services.drive.model.FileList;

import java.awt.*;
import java.io.*;
import java.security.GeneralSecurityException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.List;

public class GoogleDriveInterface {

    private static final String APPLICATION_NAME = "Security System";
    private static final JsonFactory JSON_FACTORY = GsonFactory.getDefaultInstance();
    // Directory to store user credentials for this application.
    private static final java.io.File CREDENTIALS_FOLDER //
            = new java.io.File(System.getProperty("user.home"), "credentials");
    private static final String CLIENT_SECRET_FILE_NAME = "client_secret.json";
    //
    // Global instance of the scopes required by this quickstart. If modifying these
    // scopes, delete your previously saved credentials/ folder.
    //
    private static final List<String> SCOPES = Collections.singletonList(DriveScopes.DRIVE);

    private Drive service = null;
    private Queue<String> imageQueue = new LinkedList<String>();
    private String imageQueuePath = null;
    private File currentFolder = null;
    private String currentFormattedDate = null;
    private FileList folderSearchResults = null;

    public String getImageQueuePath()
    {
        return this.imageQueuePath;
    }

    private void updateFolder(String name) throws IOException
    {
        // Triggers on boot/ reboot
        if(this.currentFormattedDate == null)
        {
            this.currentFormattedDate = name;
            String pageToken = null;
            do {
                this.folderSearchResults = service.files().list()
                        .setQ("mimeType='application/vnd.google-apps.folder'")
                        .setQ("trashed=false")
                        .setSpaces("drive")
                        .setFields("nextPageToken, files(id, name)")
                        .setPageToken(pageToken)
                        .execute();
                for(File file : this.folderSearchResults.getFiles())
                {
                    if(file.getName().compareTo(name) == 0)
                    {
                        this.currentFolder = file;
                        return;
                    }
                }
                pageToken = this.folderSearchResults.getNextPageToken();
            } while(pageToken != null);
        }
        // Search for folder with given name
        if(this.currentFormattedDate.compareTo(name) != 0 || this.currentFolder == null)
        {
            // Folder doesn't exist, create a new folder for date
            this.currentFormattedDate = name;
            File folderMetadata = new File();
            folderMetadata.setName(name);
            folderMetadata.setMimeType("application/vnd.google-apps.folder");
            File file = service.files().create(folderMetadata).setFields("id").execute();
            System.out.println("Folder ID " + file.getId() + " uploaded");
            this.currentFolder = file;
        }
    }

    private void uploadFile(String parent, String child)
    {
        try
        {
            this.updateFolder(parent);
            // Create image file
            File fileMetadata = new File();
            fileMetadata.setName(child);
            fileMetadata.setParents(Collections.singletonList(this.currentFolder.getId()));
            java.io.File filePath = new java.io.File(this.imageQueuePath + "/" + parent + "/" + child);
            FileContent mediaContent = new FileContent("image/jpeg", filePath);
            File file = service.files().create(fileMetadata, mediaContent)
                    .setFields("id").execute();
            System.out.println("File ID " + file.getId() + " uploaded");
        }
        catch (IOException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public void reduceQueue()
    {
        int IMAGES_UPLOADED_PER_DEQUEUE = 60;
        synchronized (this)
        {
            String nextImage;
            for(int i = 0; i < IMAGES_UPLOADED_PER_DEQUEUE; i++)
            {
                try
                {
                    int standardUpload = 0;
                    nextImage = this.imageQueue.remove();
                    for(int j = nextImage.length() - 1; j > 0; j--)
                    {
                        if(nextImage.charAt(j) == '/')
                        {
                            this.uploadFile(nextImage.substring(0, j), nextImage.substring(j + 1));
                            standardUpload = 1;
                            break;
                        }
                    }
                    if(standardUpload == 0)
                    {
                        this.uploadFile("", nextImage);
                    }
                }
                catch (NoSuchElementException e)
                {
                    return;
                }
            }
        }
    }

    public void queueImage(String filepath)
    {
        this.imageQueue.add(filepath);
    }

    private Credential getCredentials(final NetHttpTransport HTTP_TRANSPORT) throws IOException {

        java.io.File clientSecretFilePath = new java.io.File(CREDENTIALS_FOLDER, CLIENT_SECRET_FILE_NAME);

        if (!clientSecretFilePath.exists()) {
            throw new FileNotFoundException("Please copy " + CLIENT_SECRET_FILE_NAME //
                    + " to folder: " + CREDENTIALS_FOLDER.getAbsolutePath());
        }

        // Load client secrets.
        InputStream in = new FileInputStream(clientSecretFilePath);

        GoogleClientSecrets clientSecrets = GoogleClientSecrets.load(JSON_FACTORY, new InputStreamReader(in));

        // Build flow and trigger user authorization request.
        GoogleAuthorizationCodeFlow flow = new GoogleAuthorizationCodeFlow.Builder(HTTP_TRANSPORT, JSON_FACTORY,
                clientSecrets, SCOPES).setDataStoreFactory(new FileDataStoreFactory(CREDENTIALS_FOLDER))
                .setAccessType("offline").build();

        return new AuthorizationCodeInstalledApp(flow, new LocalServerReceiver()).authorize("user");
    }

    public GoogleDriveInterface(String tempFolder) {
        try
        {
            System.out.println("CREDENTIALS_FOLDER: " + CREDENTIALS_FOLDER.getAbsolutePath());
            // 1: Create CREDENTIALS_FOLDER
            if (!CREDENTIALS_FOLDER.exists()) {
                CREDENTIALS_FOLDER.mkdirs();

                System.out.println("Created Folder: " + CREDENTIALS_FOLDER.getAbsolutePath());
                System.out.println("Copy file " + CLIENT_SECRET_FILE_NAME + " into folder above.. and rerun this class!!");
                return;
            }
            // 2: Build a new authorized API client service.
            final NetHttpTransport HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();
            // 3: Read client_secret.json file & create Credential object.
            Credential credential = getCredentials(HTTP_TRANSPORT);
            // 5: Create Google Drive Service.
            this.service = new Drive.Builder(HTTP_TRANSPORT, JSON_FACTORY, credential) //
                    .setApplicationName(APPLICATION_NAME).build();
            this.imageQueuePath = tempFolder;
            System.out.println(this.imageQueuePath);
            if(!new java.io.File(this.imageQueuePath).exists())
            {
                new java.io.File(this.imageQueuePath).mkdirs();
            }
        }
        catch (IOException | GeneralSecurityException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        GoogleDriveInterface i = new GoogleDriveInterface(System.getProperty("user.home") + "/security-system/tmp/");
        i.queueImage("test-image.jpg");
        i.reduceQueue();
    }

}