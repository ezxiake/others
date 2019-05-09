package handle.request;

import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class testOkhttp3 {

	public static final MediaType MEDIA_TYPE_JSON = MediaType.parse("application/json; charset=utf-8");
	public static final MediaType MEDIA_TYPE_TEXT_PLAIN = MediaType.parse("text/plain; charset=utf-8");
	
	public static void main(String args[]) {
		
		OkHttpClient client = new OkHttpClient();
		

//		RequestBody body = RequestBody.create(MEDIA_TYPE_JSON, "json format string");
		
		String url = "http://localhost:11015/v3/namespaces/assuredplus/apps/AssuredPlusInstrumentation/services/queryService/methods/instrumentation/c39df255-c59d-4e04-bb6c-832090988876";
		Request request = 
				new Request.Builder()
				.url(url)
//				.post(body)
				.addHeader("Content-Type", "application/json")
				.build();
		try {
			Response response = client.newCall(request).execute();
			if(response.code() == 200) {		
				System.out.println(response.body().string());
			} else {
				System.out.println("request is failing : " + response.message());
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
