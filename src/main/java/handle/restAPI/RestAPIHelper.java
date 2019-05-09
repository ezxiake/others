package handle.restAPI;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.Map;
import net.sf.json.JSONObject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.JsonObject;

import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public class RestAPIHelper {
	private static final Logger LOG = LoggerFactory.getLogger(RestAPIHelper.class);
	
	private RestAPIService getRestAPIService(String baseURL){
		URL serviceURL = null;
		try {
			serviceURL = new URL(baseURL);
		} catch (MalformedURLException e) {
			LOG.error("Cannot connect to the oaxis endpoint",e);
			return null;
		}
    	HttpUrl httpUrl = HttpUrl.get(serviceURL);
    	if (httpUrl == null) {
    		LOG.error("Invalid URL for the service");
    		return null;
    	}
    	
    	GsonConverterFactory gsonFactory = GsonConverterFactory.create();
    	OkHttpClient.Builder builder = new OkHttpClient.Builder();
    	builder.followRedirects(false);
    	builder.connectTimeout(30, TimeUnit.SECONDS);
    	builder.readTimeout(30, TimeUnit.SECONDS);
    	OkHttpClient httpClient = builder.build();
    	httpClient.retryOnConnectionFailure();
    	
    	Retrofit retrofit = new Retrofit.Builder()
    			.client(httpClient)
    		    .baseUrl(httpUrl)
    		    //.addConverterFactory(gsonFactory)
    		    .addConverterFactory(ScalarsConverterFactory.create())
    		    .build();
    	
    	RestAPIService service = retrofit.create(RestAPIService.class);
		return service;
	}
	
	public RestAPIResponse getCookie(String username, String password){
		
		JsonObject obj = new JsonObject();
		obj.addProperty("username",username);
		obj.addProperty("password",password);
		obj.addProperty("remember_me","true");
		String req_body = obj.toString();
		Response<String> rsrp = null;
		String cookie = null;
		//RestAPIService service = getRestAPIService(Property.Oaxis_API_BaseURL);
		RestAPIService service = getRestAPIService("");
		Call<String> loginCall = service.Login(req_body);
		
		try {
			rsrp = loginCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis login service",e);
			return new RestAPIResponse(RestAPIReponseCode.Failure_GetCookie,"Failure to access the oaxis login service");
		}
		if( rsrp.code() == 200 ){
			// oaxis may return multi header with name "set-cookie", retrieve the correct one
			List<String> set_cookies = rsrp.raw().headers().values("set-cookie");
			for(String setcookie : set_cookies){
				if(setcookie.startsWith("JSESSIONID=")){
					cookie = setcookie.split(";")[0];
					break;
				}
			}
		}
		else{
			LOG.error("oaxis login service return errorcode:"+rsrp.code());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,cookie);
	}
	
	public RestAPIResponse getCode(String cookie, String clientID, String redirect_url, String scope, String response_type){
		Response<String> rsrp = null;
		//RestAPIService service = getRestAPIService(Property.Oaxis_API_BaseURL);
		RestAPIService service = getRestAPIService("");
		Call<String> codeCall = service.GetCode(cookie,clientID,redirect_url,scope,response_type);
		String code = null;
		try {
			rsrp = codeCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis requery code service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.Failure_GetCode,"Failure to access the oaxis requery code service");
		}
		if( rsrp.code() == 302 ){
			String rsp_location = rsrp.raw().header("location");
			if(rsp_location.isEmpty()){
				LOG.error("Cannot find the location header from oaxis getCode service");
				return new RestAPIResponse(RestAPIReponseCode.Failure_GetCode,"Cannot find the location header from oaxis getCode service");
			}
			try {
				URL url = new URL(rsp_location);
				code = url.getQuery().split("=")[1];
			} catch (MalformedURLException e) {
				LOG.error("Parse the location url error when get oaxis code",e);
				e.printStackTrace();
				return new RestAPIResponse(RestAPIReponseCode.Failure_GetCode,"Parse the location url error when get oaxis code");
			}
		}
		else{
			LOG.error("oaxis query code service return errorcode:"+rsrp.code());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,code);
	}
	
	public RestAPIResponse getAccessToken(String cookie,String client_id, String client_secret, String code){
		JsonObject obj = new JsonObject();
		obj.addProperty("client_id",client_id);
		obj.addProperty("client_secret",client_secret);
		obj.addProperty("code",code);
		String req_body = obj.toString();
		Response<String> rsrp = null;
//		String accessToken = null;
				
		RestAPIService service = getRestAPIService("");
		Call<String> accessTokenCall = service.GetAccessToken(cookie, req_body);
		LOG.info("URL="+accessTokenCall.request().url().toString() + " Header="+ accessTokenCall.request().headers().toString() + " Body="+ req_body);//Used to be LOG.debug
		
		try {
			rsrp = accessTokenCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis requery accesstoken service",e);
			return new RestAPIResponse(RestAPIReponseCode.Failure_GetAccesstoken,"Failure to access the oaxis requery accesstoken service");
		}
		
		if(rsrp.code() != 200){
			LOG.error("Failure to get Access Token, code:"+rsrp.code()+"message:"+rsrp.message());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,rsrp.body());
	}
	
	public RestAPIResponse refreshToken(String client_id, String client_secret){
		JsonObject obj = new JsonObject();
		obj.addProperty("clientID",client_id);
		obj.addProperty("clientSecret",client_secret);
		String req_body = obj.toString();
		
		Response<String> rsrp = null;
		
		RestAPIService service = getRestAPIService("");
		Call<String> accessTokenCall = service.RefreshToken(req_body);
		
		try {
			rsrp = accessTokenCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis refresh token service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.Failure_RefreshAccesstoken,"Failure to access the oaxis refresh token service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to refresh Token, code:"+rsrp.code()+"message:"+rsrp.message());
			return new RestAPIResponse(rsrp.code(), rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("Refresh token success");
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, objRoot.getJSONObject("data").toString());
		} else {
			LOG.error("Failure to refresh token from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisResponseInsideCodeUnequal200Error, objRoot.getString("message"));
		}
	}
	
	public RestAPIResponse getMasterUserInfo(String accessToken){
		Response<String> rsrp = null;
		
		RestAPIService service = getRestAPIService("");
		Call<String> MasterUserInfoCall = service.GetMasterAccountInfo("Bearer "+accessToken);
		
		try {
			rsrp = MasterUserInfoCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis masterUserinfo service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.Failure_GetMasterInfo,"Failure to access the oaxis masterUserinfo service");
		}
		if(rsrp.code()!= 200){
			LOG.error("Failure access getMasterUserInfo from Oaxis response,code="+rsrp.code()+" message="+rsrp.message()+" accessToken="+accessToken);
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		return new RestAPIResponse(200,rsrp.body());
	}
	
	public RestAPIResponse createSubAccount(
			String accessToken, 
			String name
			)
	{
		JsonObject obj = new JsonObject();
		obj.addProperty("cloudAccessToken",accessToken);
		obj.addProperty("userName",name);
		String subAccountinfo = obj.toString();
		
		LOG.info("Create the SubAccount with body:"+subAccountinfo);
		
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> createSubAccountCall = service.CreateSubAccount(subAccountinfo);
		
		try {
			rsrp = createSubAccountCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis createSubAccount service",e);
			return new RestAPIResponse(RestAPIReponseCode.Failure_CreateSubAccount,"Failure to access the oaxis createSubAccount service");
		}
		LOG.info("rsrp.code() : " + rsrp.code());//Used to be LOG.debug
		if(rsrp.code()!=200){
			LOG.error("Failure to access createSubAccountCall, code="+rsrp.code()+" message="+rsrp.message()+" accessToken="+accessToken+" subAccountinfo="+subAccountinfo);
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		} else {
			JSONObject objRoot = JSONObject.fromObject(rsrp.body());
			if(objRoot.getInt("code") == 200) {
				LOG.info("Create sub user success:" + rsrp.body());
				return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, objRoot.getJSONObject("data").toString());
			} else {
				LOG.error("Failure to access createSubAccountCall from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message") + " accessToken=" + accessToken + " subAccountinfo=" + subAccountinfo);
				return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
			}
		}
	}
	
	public RestAPIResponse ActiveDevice(String userToken, String bindCode){
		JsonObject obj = new JsonObject();
		obj.addProperty("accessToken",userToken);
		obj.addProperty("bindCode",bindCode);
		String deviceInfo = obj.toString();
		LOG.info("Try to active the device with body:"+deviceInfo);
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> activeDeviceCall = service.ActiveDevice(deviceInfo);

		try {
			rsrp = activeDeviceCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis activeDeviceCall service",e);
			return new RestAPIResponse(RestAPIReponseCode.Failure_ActiveDevice,"Failure to access the oaxis activeDeviceCall service");
		}
		if(rsrp.code()!=200){
			LOG.error("Failure to bind device, code:"+rsrp.code()+"message:"+rsrp.message());
			return new RestAPIResponse(rsrp.code(), rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("The Device bind success for user:"+deviceInfo);
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, objRoot.getJSONObject("data").toString());
		} else {
			LOG.error("Failure to bind the device from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisResponseInsideCodeUnequal200Error, objRoot.getString("message"));
		}
	}
	
	public RestAPIResponse DeActiveDevice(String userToken, String deviceID){
		JsonObject obj = new JsonObject();
		obj.addProperty("accessToken",userToken);
		obj.addProperty("deviceID",deviceID);
		String deviceInfo = obj.toString();
		LOG.info("Try to deactive the device with body:"+deviceInfo);
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deactiveDeviceCall = service.DeActiveDevice(deviceInfo);

		try {
			rsrp = deactiveDeviceCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deactiveDeviceCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.Failure_DeactiveDevice,"Failure to access the oaxis deactiveDeviceCall service");
		}
		if(rsrp.code()!=200 || rsrp.code()!=427){
			LOG.error("Failure to unbind device, code:"+rsrp.code()+"message:"+rsrp.message());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200 || rsrp.code()==427){
			LOG.info("The Device unbind success for user:"+deviceInfo);
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,"success");
		} else {
			LOG.error("Failure to unbind the device from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisResponseInsideCodeUnequal200Error, objRoot.getString("message"));
		}
	}
	
	public RestAPIResponse DeleteUser(String accessToken, int userID, String userToken){
		JsonObject obj = new JsonObject();
		obj.addProperty("cloudAccessToken",accessToken);
		obj.addProperty("userID",userID);
		obj.addProperty("userToken",userToken);
		String userInfo = obj.toString();
		LOG.info("Delete user - Try to delete the user with body:"+userInfo);
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deleteUser = service.DeleteUser(userInfo);

		try {
			rsrp = deleteUser.execute();
		}catch(IOException e){
			LOG.error("Delete user - Failure to access the oaxis DeleteUser service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.Failure_DeactiveDevice,"Failure to access the oaxis DeleteUser service");
		}
		if(rsrp.code()!=200){
			LOG.error("Failure to delete user, code:"+rsrp.code()+"message:"+rsrp.message());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("The user delete success for user:"+userInfo);
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,"success");
		} else {
			LOG.error("Failure to delete user from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisResponseInsideCodeUnequal200Error, objRoot.getString("message"));
		}
	}
	
	public RestAPIResponse CreateAWS_SQS(String accessToken,String master_account_id, String aws_account_id){
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		JsonObject obj = new JsonObject();
		obj.addProperty("aws_account",aws_account_id);
		String body = obj.toString();
		Call<String> createSQSCall = service.CreateAWS_SQS("Bearer "+accessToken, master_account_id, body);
		
		try {
			rsrp = createSQSCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis CreateAWS_SQS service",e);
			return new RestAPIResponse(RestAPIReponseCode.Failure_CreateSQS,"Failure to access the oaxis CreateAWS_SQS service");
		}
		if(rsrp.code()!=200){
			LOG.error("Failure to active device:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		LOG.info("create master user sqs return, code="+rsrp.code()+" message="+rsrp.message()+" body="+rsrp.body());//Used to be LOG.debug
		return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,"success");
	}
	
	public RestAPIResponse getDeviceConfig(String userToken, String deviceID){
		Map<String, String> map = new HashMap<String, String>();
		map.put("accessToken", userToken);
		map.put("deviceID", deviceID);
		
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> DeviceConfigCall = service.getDeviceConfig(map);

		try {
			rsrp = DeviceConfigCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis getDeviceConfig service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis DeviceConfigCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to get device config: code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("Query device config info success."+objRoot.getString("data"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,objRoot.getString("data"));
		} else {
			LOG.error("Failure to get device config from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}
	
/*	public RestAPIResponse setDeviceConfig(String userToken, String deviceID, OaxisDeviceConfigInfo deviceConfig){
		
		JsonObject obj = new JsonObject();
		obj.addProperty("accessToken",userToken);
		obj.addProperty("deviceID",deviceID);
		
		if(deviceConfig.getName() != null) {obj.addProperty("name",deviceConfig.getName());}
		if(deviceConfig.getSim() != null) {obj.addProperty("sim",deviceConfig.getSim());}
		if(deviceConfig.getTimeZone() != null) {obj.addProperty("timeZone",deviceConfig.getTimeZone());}
		if(deviceConfig.getRefusePhone() != -1) {obj.addProperty("refusePhone",deviceConfig.getRefusePhone());}
		if(deviceConfig.getCallLocation() != -1) {obj.addProperty("callLocation",deviceConfig.getCallLocation());}
		if(deviceConfig.getPowerOffLocation() != -1) {obj.addProperty("powerOffLocation",deviceConfig.getPowerOffLocation());}
		if(deviceConfig.getLowerBatteryLocation() != -1) {obj.addProperty("lowerBatteryLocation",deviceConfig.getLowerBatteryLocation());}
		if(deviceConfig.getSceneMode() != -1) {obj.addProperty("sceneMode",deviceConfig.getSceneMode());}
		if(deviceConfig.getGpsFrequency() != -1) {obj.addProperty("gpsFrequency",deviceConfig.getGpsFrequency());}
		if(deviceConfig.getLowerBatteryThreshold() != -1) {obj.addProperty("lowerBatteryThreshold",deviceConfig.getLowerBatteryThreshold());}
		
//		if(obj.entrySet().size() == 2) {
//			LOG.error("bad request, invalid json");
//			return new RestAPIResponse(RestAPIReponseCode.InvalidJsonFormat,"bad request, invalid json");
//		}

		String objStr = obj.toString();
		LOG.info("Try to post the device config with body:" + objStr);//Used to be LOG.debug
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deviceConfigCall = service.setDeviceConfig(objStr);

		try {
			rsrp = deviceConfigCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deviceConfigCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis deviceConfigCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to set device config: code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("The Device post config success for user:" + objStr);
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,"success");
		} else {
			LOG.error("Failure to set device config from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}*/
	
	public RestAPIResponse getDnd(String userToken, String deviceID){
		Map<String, String> map = new HashMap<String, String>();
		map.put("accessToken", userToken);
		map.put("deviceID", deviceID);
		
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> DeviceDndCall = service.getDnd(map);

		try {
			rsrp = DeviceDndCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis DeviceDndCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis DeviceDndCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to get device dnd:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("Query device dnd info success."+objRoot.getString("data"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,objRoot.getString("data"));
		} else {
			LOG.error("Failure to get device dnd from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}
	
/*	public RestAPIResponse setDeviceDnd(String userToken, String deviceID, OaxisDndInfo deviceDnd){
		
		JsonObject obj = new JsonObject();
		obj.addProperty("accessToken",userToken);
		obj.addProperty("deviceID",deviceID);
		obj.addProperty("sec1", deviceDnd.getSec1());
		obj.addProperty("sec2", deviceDnd.getSec2());
		obj.addProperty("repeatExpression", deviceDnd.getRepeatExpression());
		
		String objStr = obj.toString();
		LOG.info("Try to post the device dnd with body:" + objStr);//Used to be LOG.debug
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deviceDndCall = service.setDeviceDnd(objStr);

		try {
			rsrp = deviceDndCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deviceDndCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis deviceDndCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to set device dnd:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("The Device post dnd success for user:" + objRoot.getString("data"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, objRoot.getString("data"));
		} else {
			LOG.error("Failure to set device dnd from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}*/
	
	public RestAPIResponse getLocation(String userToken, String deviceID){
		Map<String, String> map = new HashMap<String, String>();
		map.put("accessToken", userToken);
		map.put("deviceID", deviceID);
		
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deviceLocationCall = service.getLocation(map);

		try {
			rsrp = deviceLocationCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deviceLocationCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis deviceLocationCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to get location:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("Query device location info success."+rsrp.body());
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, rsrp.body());
		} else {
			LOG.error("Failure to get location from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
		
	}
	
	public RestAPIResponse getWhitelist(String userToken, String deviceID){
		Map<String, String> map = new HashMap<String, String>();
		map.put("accessToken", userToken);
		map.put("deviceID", deviceID);
		
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deviceWhitelistCall = service.getWhitelist(map);

		try {
			rsrp = deviceWhitelistCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deviceWhitelistCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis deviceWhitelistCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to get whitelist:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("Query device whitelist info success."+objRoot.getString("data"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess,objRoot.getString("data"));
		} else {
			LOG.error("Failure to get whitelist from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}
	
	public RestAPIResponse setDeviceWhitelistNew(String userToken, String deviceID, String name, String mobile){
		
		JsonObject obj = new JsonObject();
		obj.addProperty("accessToken",userToken);
		obj.addProperty("deviceID",deviceID);
		if(name != null) {obj.addProperty("name", name);}
		obj.addProperty("mobile", mobile);
		
		String objStr = obj.toString();
		LOG.info("Try to post the device whitelist new with body:" + objStr);
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deviceWhitelistNewCall = service.setDeviceWhitelistNew(objStr);

		try {
			rsrp = deviceWhitelistNewCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deviceWhitelistNewCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis deviceWhitelistNewCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to set whitelist new:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("The Device post whitelist new success for user:" + objRoot.getString("data"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, objRoot.getString("data"));
		} else {
			LOG.error("Failure to set whitelist new from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}
	
	public RestAPIResponse setDeviceWhitelistUpdate(String userToken, String deviceID, String name, String mobile, int whitelistID){
		
		JsonObject obj = new JsonObject();
		obj.addProperty("accessToken",userToken);
		obj.addProperty("deviceID",deviceID);
		if(name != null) {obj.addProperty("name", name);}
		obj.addProperty("mobile", mobile);
		obj.addProperty("whitelistID", whitelistID);
		
		String objStr = obj.toString();
		LOG.info("Try to post the device whitelist update with body:" + objStr);//Used to be LOG.debug
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deviceWhitelistUpdateCall = service.setDeviceWhitelistUpdate(objStr);

		try {
			rsrp = deviceWhitelistUpdateCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deviceWhitelistUpdateCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis deviceWhitelistUpdateCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to get whitelist update:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("The Device post whitelist update success for user:" + objRoot.getString("data"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, objRoot.getString("data"));
		} else {
			LOG.error("Failure to set whitelist update from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}
	
	public RestAPIResponse setDeviceWhitelistDelete(String userToken, String deviceID, int whitelistID){
		
		JsonObject obj = new JsonObject();
		obj.addProperty("accessToken",userToken);
		obj.addProperty("deviceID",deviceID);
		obj.addProperty("whitelistID", whitelistID);
		
		String objStr = obj.toString();
		LOG.info("Try to post the device whitelist delete with body:" + objStr);//Used to be LOG.debug
		Response<String> rsrp = null;
		RestAPIService service = getRestAPIService("");
		Call<String> deviceWhitelistDeleteCall = service.setDeviceWhitelistDelete(objStr);

		try {
			rsrp = deviceWhitelistDeleteCall.execute();
		}catch(IOException e){
			LOG.error("Failure to access the oaxis deviceWhitelistDeleteCall service",e);
			e.printStackTrace();
			return new RestAPIResponse(RestAPIReponseCode.OaxisAdapterExceptionError,"Failure to access the oaxis deviceWhitelistDeleteCall service");
		}
		
		if(rsrp.code()!=200){
			LOG.error("Failure to whitelist delete:code="+rsrp.code()+" message:"+rsrp.message()+" body:"+rsrp.body());
			return new RestAPIResponse(rsrp.code(),rsrp.message());
		}
		
		JSONObject objRoot = JSONObject.fromObject(rsrp.body());
		if(objRoot.getInt("code") == 200){
			LOG.info("The Device post whitelist delete success for user:" + objRoot.getString("data"));
			return new RestAPIResponse(RestAPIReponseCode.OaxisSuccess, objRoot.getString("data"));
		} else {
			LOG.error("Failure to whitelist delete from Oaxis response, code=" + objRoot.getString("code") + " message="+ objRoot.getString("message"));
			return new RestAPIResponse(objRoot.getInt("code"), objRoot.getString("message"));
		}
	}
}
