package handle.restAPI;

import handle.json.JsonUtil;

public class test {

	public static void main(String args[]) {
		
		final StringBuffer onboardResult = new StringBuffer();
		RestAPIHelper apiHelper = new RestAPIHelper();
		
		RestAPIResponse apiResult = apiHelper.createSubAccount("", "");
		
		if(apiResult.getCode() != RestAPIReponseCode.OaxisSuccess){
//			LOG.error("Failure to create sub account,code:"+apiResult.getCode()+" message:"+apiResult.getMessage());
			onboardResult.append(JsonUtil.toJson(new RestAPIResponse(apiResult.getCode(),apiResult.getMessage())));
		}
		
		RestAPIResponse onboardResultObj = null;
		if(onboardResult.length() == 0){
			onboardResultObj = null;
		}
		else{
			onboardResultObj = JsonUtil.fromJson(onboardResult.toString(),RestAPIResponse.class);
		}
		
		System.out.println(onboardResultObj.getCode());
		System.out.println(onboardResultObj.getMessage());
	}
}
