package handle.IO;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class DataStreamDemo {
	public static void main(String[]args) {
		
		Member[] members = { new Member("Justin", 90), new Member("momor", 95), new Member("Bush", 88) };

		try {

			DataOutputStream dataOutputStream = new DataOutputStream(new FileOutputStream("DataStreamDemo.txt"));

			for (Member member : members) {
				// write UTF string
				dataOutputStream.writeUTF(member.getName());
				// write int data
				dataOutputStream.writeInt(member.getAge());
			}

			// All data to the destination
			dataOutputStream.flush();
			dataOutputStream.close();

			DataInputStream dataInputStream = new DataInputStream(new FileInputStream("DataStreamDemo.txt"));

			// Read the data and restore it to the object
			for (int i = 0; i < members.length; i++) {
				// read UTF string
				String name = dataInputStream.readUTF();
				// read out int data
				int score = dataInputStream.readInt();
				members[i] = new Member(name, score);
			}

			dataInputStream.close();

			// Displays the restored data
			for (Member member : members) {
				System.out.printf("%s\t%d%n", member.getName(), member.getAge());
			}

		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}

class Member {
	private String name;
    private int age;
    public Member() {}
	public Member(String name, int age) {
		this.name = name;
		this.age = age;
    }
    public void setName(String name){
        this.name = name;
    }
    public void setAge(int age) {
        this.age = age;
    }
    public String getName() {
        return name;
    }
    public int getAge() {
        return age;
    }
}