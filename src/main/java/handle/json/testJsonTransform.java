package handle.json;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;
import java.util.Map;

import org.yaml.snakeyaml.Yaml;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class testJsonTransform {

	public static void main(String args[]) throws FileNotFoundException {
		
		/*
		 * com.google.gson.JsonObject
		 * 
		 * */
		
		Gson gson = new Gson();
		
		// string to object
		testBean tb = gson.fromJson("{name:\"xiao\",age:18,list:{a:1,b:2,c:3}}", testBean.class);
		
		// object to string
		String s = gson.toJson(tb);
		
		System.out.println(tb.getName());
		System.out.println(tb.getAge());
		System.out.println(tb.getList().getA());
		System.out.println(tb.getList().getB());
		System.out.println(tb.getList().getC());
		System.out.println(s);
		
		// JsonObject
		JsonObject obj = new JsonObject();
		obj.addProperty("a", "aa");
		obj.addProperty("b", "bb");
		obj.addProperty("c", obj.toString());
		String responseString = obj.toString();
		System.out.println(responseString);
			

		
		/*
		 * net.sf.json.JSONObject
		 * 
		 * */
		
		String fileInput;
		if(args.length == 0) {
			fileInput = "test.yaml";
		} else {
			fileInput = args[0];
		}

//		String directory = new File(fileInput).getParent();
		
		InputStream input = new FileInputStream(fileInput);
		
		Yaml yaml = new Yaml();
		
		// yaml to HashMap
		Map<String, Object> object = (Map<String, Object>) yaml.load(input);
		
		// HashMap to JSONObject
		JSONObject jsonRoot = JSONObject.fromObject(object);
		
		JSONObject settings4MsgSend = jsonRoot.getJSONObject("settings4MsgSend");
		System.out.println(settings4MsgSend.getString("sqs"));
		System.out.println();
//		https://sqs.ap-southeast-1.amazonaws.com/991189208874/Oaxis_Test
		
		JSONObject extSubGeozilla = jsonRoot.getJSONObject("extSubGeozilla");
		JSONArray ja_channel = extSubGeozilla.getJSONArray("channels");
		
		for(int i = 0; i < ja_channel.size(); i++) {
			System.out.println(ja_channel.get(i));
		}
		
		System.out.println(); //////////////////////////////////////////////
		
		// string to JSONObject
		JSONObject JSONObj = new JSONObject().fromObject("{a:123, b:\"adf\"}");
		JSONObj.put("timeCurrent", "timeCurrent");
		JSONObj.put("pubnubTimeToken", "pubnubTimeToken");
		System.out.println(JSONObj);
		
		// Iterator
		System.out.println("test iterator start +++");
		Iterator it = JSONObj.keys();
		while(it.hasNext()) {
			String tmp = (String)it.next();
			System.out.println(tmp);
			System.out.println(JSONObj.getString(tmp));
		}
		System.out.println("test iterator stop +++");
		
		System.out.println(); //////////////////////////////////////////////
		
		// JSONObject
		JSONObject jj = new JSONObject();
		jj.put("test", 111);
		jj.put("name", "ke");
		System.out.println(jj);
		
		System.out.println(); //////////////////////////////////////////////
		
		StandardCharsets.UTF_8.decode(ByteBuffer.wrap("".getBytes())).toString();
		StandardCharsets.UTF_8.encode("").toString();
	}
}

class testBean {
	
	String name = "ke";
	int age = 20;
	subBean list;
	
	
	public subBean getList() {
		return list;
	}
	

	public void setList(subBean list) {
		this.list = list;
	}
	

	public testBean() {}

	public String getName() {
		return name;
	}
	

	public void setName(String name) {
		this.name = name;
	}
	

	public int getAge() {
		return age;
	}
	

	public void setAge(int age) {
		this.age = age;
	}
	
}

class subBean {
	
	int a = 0;
	int b = 0;
	int c = 0;
	
	public subBean() {}

	public int getA() {
		return a;
	}
	

	public void setA(int a) {
		this.a = a;
	}
	

	public int getB() {
		return b;
	}
	

	public void setB(int b) {
		this.b = b;
	}
	

	public int getC() {
		return c;
	}
	

	public void setC(int c) {
		this.c = c;
	}
	
}