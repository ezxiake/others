package handle.multiThreading;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class testRunnable implements Runnable{

	private String flag;
	private static List tn = new ArrayList<Thread>();
	
	public static void main(String args[]) {
		
//		BlockingQueue<String> messageIdList = new LinkedBlockingQueue<String>();
		
		Thread t1 = new Thread(new testRunnable("1"));
		Thread t2 = new Thread(new testRunnable("2"));
		
//		t1.setDaemon(true);  // if run this code, then this thread will dependency main process , main thread exit - sub thread also exit. 
//		t2.setDaemon(true);
		
		tn.add(t1);
		tn.add(t2);
		
		for(int i=0; i<tn.size(); i++) {
			((Thread)tn.get(i)).start();
		}
		
//		System.exit(0); // if run this code,then all thread will be exit.
		
		new Thread() {
			public void run() {
				System.out.println(Thread.currentThread().getName() + " - I am a sub thread.");
			}
		}.start();
		
//		Thread main = Thread.currentThread();
//		main.interrupt();
//		System.exit(0);
		
	}

	@Override
	public void run() {
		// TODO Auto-generated method stub
		System.out.println(Thread.currentThread().getName() + flag);
		
		try {
			Thread.sleep(3000);
//			System.exit(0);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public testRunnable(String flag) {
		this.flag = flag;
	}

	
}