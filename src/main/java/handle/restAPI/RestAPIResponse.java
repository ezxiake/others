package handle.restAPI;


public class RestAPIResponse {
	private int code = 0;
	private String message = "";
	
	public RestAPIResponse(){}
	
	public RestAPIResponse(int code, String message){
		this.code = code;
		this.message = message;
	}
	
	public int getCode() {
		return code;
	}
	public void setCode(int code) {
		this.code = code;
	}
	public String getMessage() {
		return message;
	}
	public void setMessage(String message) {
		this.message = message;
	}
}