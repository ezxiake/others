package handle.IO;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

public class InputStreamAndOutputStream {

	public static void main(String[] args){

        long start1 = System.currentTimeMillis();
        withoutBufferedDemo();
        long end1 = System.currentTimeMillis();
        System.out.println("Time1 : "+(end1 - start1)+"ms");
        
        long start2 = System.currentTimeMillis();
        userDefinedBufferedDemo();
        long end2 = System.currentTimeMillis();
        System.out.println("Time2 : "+(end2 - start2)+"ms");
        
        long start3 = System.currentTimeMillis();
        BufferedDemo();
        long end3 = System.currentTimeMillis();
        System.out.println("Time3 : "+(end3 - start3)+"ms");
	}

    public static void withoutBufferedDemo() {

        FileInputStream fis = null;
        FileOutputStream fos = null;
        try {
            fis = new FileInputStream("src\\main\\java\\handle\\IO\\io.jpg");
            fos = new FileOutputStream("InputStreamAndOutputStream_1.jpg");
            byte[] copy = new byte[1024];
            int len = 0;
            while((len = fis.read(copy))!=-1) {
            	fos.write(copy, 0, len);
            }
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("Copy file exception");
        } finally {
            try {
                if(fis != null) fis.close();
            } catch (IOException e) {
                e.printStackTrace();
                throw new RuntimeException("Read the flow");
            }
        }
    }

    public static void userDefinedBufferedDemo() {

        MyBufferedInputStream bis = null;
        BufferedOutputStream  bos = null;
        try {
            bis = new MyBufferedInputStream(new FileInputStream("src\\main\\java\\handle\\IO\\io.jpg"));//匿名类，传入一个InputStream流对象
            bos = new BufferedOutputStream(new FileOutputStream("InputStreamAndOutputStream_2.jpg"));
            int buf = 0;
            while((buf = bis.MyRead())!=-1) {
                bos.write(buf);
            }
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("Copy is failing");
        } finally {
            try {
                if(bis!=null)  {
                    bis.myClose();
                    bos.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    
    public static void BufferedDemo() {

        BufferedInputStream bis = null;
        BufferedOutputStream  bos = null;
        try {
            bis = new BufferedInputStream(new FileInputStream("src\\main\\java\\handle\\IO\\io.jpg"));
            bos = new BufferedOutputStream(new FileOutputStream("InputStreamAndOutputStream_3.jpg"));
            int buf = 0;
            while((buf = bis.read())!=-1) {
                bos.write(buf);
            }
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("Copy is failing");
        } finally {
            try {
                if(bis!=null)  {
                    bis.close();
                    bos.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

//user defined BufferedInputStream
class MyBufferedInputStream  {
    private InputStream in;
    private byte [] buf = new byte[1024*4];
    private int count = 0, pos = 0;
    public MyBufferedInputStream(InputStream in){
        this.in = in;
    }

    public  int MyRead() throws IOException{

        if(count==0) {
            count = in.read(buf);
            pos = 0;
            byte b = buf[pos];
            count--;
            pos++;
            return b&255;       // Promoted to integer type, Add 0 to the first three bytes。Avoid `1111 1111 1111 1111`
        } else if(count > 0) {
            byte b = buf[pos];
            pos++;
            count--;
            return b&0xff;      // Promoted to integer type, Add 0 to the first three bytes。Avoid `1111 1111 1111 1111`
        }

        return -1;
    }

    public void myClose() throws IOException{
        in.close();
    }

}
