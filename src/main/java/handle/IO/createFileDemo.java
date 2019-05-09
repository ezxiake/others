package handle.IO;

import java.io.File;

public class createFileDemo{  
    public static void main(String[] args) {  
       
        File f=new File("createFileDemo.txt");  
        try{
        	
        	// If and only if there is no file with the name specified by this abstract pathname, a new empty file is inseparably created.
        	f.createNewFile();
            
            System.out.println("Partition size"+f.getTotalSpace()/(1024*1024*1024)+"G");
            
            // Create the directory specified by this abstract pathname, including all required but nonexistent parent directories.
//            f.mkdirs();
            // Delete the file or directory represented by this abstract pathname
//            f.delete();
            
            
            // Returns the name of the file or directory represented by this abstract pathname.
            System.out.println("file name "+f.getName());
           
            // Returns the pathname string of the parent directory of this abstract pathname, or null if this pathname does not specify a parent directory.
            System.out.println("File parent directory string "+f.getParent());
            
        }catch (Exception e) {  
            e.printStackTrace();  
        }  
    }    
}