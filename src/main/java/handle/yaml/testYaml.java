package handle.yaml;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Map;

import org.yaml.snakeyaml.Yaml;

import net.sf.json.JSONObject;

public class testYaml {

	public static void main(String args[]) throws FileNotFoundException {
		
//		if(args.length == 0) {
//			System.out.println("args length is zero.");
//			return;
//		}
		
		
		Yaml yaml = new Yaml();
		Map<String, Object> object = (Map<String, Object>) yaml.load(new FileInputStream("test.yaml"));
		JSONObject jsonRoot = JSONObject.fromObject(object);
		System.out.println(jsonRoot);
		
		
	}
	
}
