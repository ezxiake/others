package handle.IO;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.Scanner;

public class WriterAndReaderDemo {

	private static String filename = "WriterAndReaderDemo.txt";
	
    public static void main(String[] args) {
    	
//        sop("test entry : ");  
//        Scanner in = new Scanner(System.in);  
//        String source = in.next();  
//        sop("test entry again : ");  
//        String destination = in.next();  
//        in.close();

    	fileWriter();
    	
    	System.out.println("===== cut-off rule : fileReaderByCharacters() =====");
    	
    	fileReaderByCharacters();
    	
    	System.out.println("===== cut-off rule : fileReaderBySingleCharacter() =====");
    	
    	fileReaderBySingleCharacter();
    	
    	System.out.println("===== cut-off rule : bufferedWriter() =====");
    	
    	bufferedWriter();
    	
    	System.out.println("===== cut-off rule : bufferedReader() =====");
    	
    	bufferedReader();
    }

    private static void fileWriter() {

		try {
			FileWriter fw = new FileWriter(filename);

	        // invoke the write method to write a string to the stream
	        fw.write("hello world!\r\nhoho\r\n");

	        // Refresh the data in the stream object buffer, push the data to the destination
	        fw.flush();

	        // Closes the stream resource but refreshes the data in the internal buffer before closing. When we finish inputting, we must close ();
	        fw.write("first_test");

	        // The difference between `flush` and `close` : `flush` refresh can continue to enter, `close` refresh can not continue typing.
	        fw.close();

	        // Passing a parameter `true` that represents not overwriting existing data. And continue writing the data at the end of the existing data
            FileWriter fw2 = new FileWriter(filename, true);
//            FileWriter fw2 = new FileWriter(filename);
            fw2.write(" is charactor table?");
            fw2.close();

		} catch (IOException e) {
			sop(e.toString());
		}

    }

    // Reads characters into an array.
    private static void fileReaderByCharacters() {

        try {

            FileReader fr = new FileReader(filename);

            char [] buf = new char[6];
            int num = 0;
            while((num = fr.read(buf))!=-1) {
                sop(new String(buf, 0, num));
            }

            sop('\n');
            fr.close();
            
        } catch (FileNotFoundException e) {
        	sop(e.toString());
        } catch (IOException e) {
            sop(e.toString());
        }
    }

    // Reads a single character.
    private static void fileReaderBySingleCharacter() {

        try {
 
            FileReader fr = new FileReader(filename);

            int ch = 0;
            while ((ch=fr.read())!=-1) {
                sop((char)ch);
            }
            sop('\n');
            fr.close();  

        } catch (FileNotFoundException e) {
        	sop(e.toString());
        } catch (IOException e) {
            sop(e.toString());
        }
    }

    private static void bufferedWriter() {
    	try {
/*
    		FileWriter fw = new FileWriter(filename, true);
            BufferedWriter bfw = new BufferedWriter(fw);  
*/
    		
    		BufferedWriter bfw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filename, true), "UTF-8"));
            bfw.write("\r\n");  // == bfw.newLine();
            
            for(int x = 1; x < 5; x++) {
            	bfw.write("test the BufferedWriter write()" + x);
            	bfw.newLine();
            	bfw.append(null).append(" cut-off line ").append(null);
            	bfw.newLine(); //  == bfw.write("\r\n") , it is a cross-platform line break
            	bfw.flush();
            }

            bfw.flush();
            bfw.close();
//            fw.close();
    	} catch (IOException e) {
            sop(e.toString());
        }
    }
    
    private static void bufferedReader() {
    	
    	try {
    		FileReader fr = new FileReader(filename);
            BufferedReader bfr = new BufferedReader(fr);

            for(;;) {
                String s = bfr.readLine();
                if(s==null) break;
                System.out.println(s);
            }
              
            bfr.close();
            fr.close();
    	} catch (FileNotFoundException e) {
        	sop(e.toString());
        } catch (IOException e) {
            sop(e.toString());
        }

    }

    private static void sop(Object obj)
    {
        System.out.println(obj);
    }
}