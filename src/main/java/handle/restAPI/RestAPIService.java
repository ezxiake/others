package handle.restAPI;

import java.util.HashMap;
import java.util.Map;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.http.*;

public interface RestAPIService {
	
	
	@POST("oauth2/accessToken")
	@Headers("Content-Type: application/json")
	Call<String> RefreshToken(@Body String body);
	
	@POST("user/create")
	@Headers("Content-Type: application/json")
	Call<String> CreateSubAccount(@Body String body);
	
	@POST("device/bind")
	@Headers("Content-Type: application/json")
	Call<String> ActiveDevice(@Body String body);
	
	@POST("device/unbind")
	@Headers("Content-Type: application/json")
	Call<String> DeActiveDevice(@Body String body);
	
	@POST("user/delete")
	@Headers("Content-Type: application/json")
	Call<String> DeleteUser(@Body String body);
	
	@GET("device/config")
	@Headers("Content-Type: application/json")
	Call<String> getDeviceConfig(@QueryMap Map<String, String> map);
	
	@POST("device/config")
	@Headers("Content-Type: application/json")
	Call<String> setDeviceConfig(@Body String body);
	
	@GET("device/dnd")
	@Headers("Content-Type: application/json")
	Call<String> getDnd(@QueryMap Map<String, String> map);
	
	@POST("device/dnd")
	@Headers("Content-Type: application/json")
	Call<String> setDeviceDnd(@Body String body);
	
	@GET("device/location")
	@Headers("Content-Type: application/json")
	Call<String> getLocation(@QueryMap Map<String, String> map);
	
	@GET("device/whitelist")
	@Headers("Content-Type: application/json")
	Call<String> getWhitelist(@QueryMap Map<String, String> map);
	
	@POST("device/whitelist/new")
	@Headers("Content-Type: application/json")
	Call<String> setDeviceWhitelistNew(@Body String body);
	
	@POST("device/whitelist/update")
	@Headers("Content-Type: application/json")
	Call<String> setDeviceWhitelistUpdate(@Body String body);
	
	@POST("device/whitelist/delete")
	@Headers("Content-Type: application/json")
	Call<String> setDeviceWhitelistDelete(@Body String body);
	
	@POST("internal/v1/user/login")
	@Headers("Content-Type: application/json")
	Call<String> Login(@Body String loginbody);
	
	@GET("v3/oauth2/auth")
	@Headers("Content-Type: application/json")
	Call<String> GetCode(
			@Header("Cookie") String cookie,
			@Query("client_id") String client_id,
			@Query("redirect_uri") String redirect_uri,
			@Query("scope") String scope,
			@Query("response_type") String response_type
			);
	
	@POST("v3/oauth2/token")
	@Headers("Content-Type: application/json")
	Call<String> GetAccessToken( @Header("Cookie") String cookie, @Body String body );
	
	@GET("v3/user")
	@Headers("Content-Type: application/json")
	Call<String> GetMasterAccountInfo( @Header("Authorization") String accessToken );
	
	@POST("v3/amazon/{master_account_id}/sqs")
	@Headers("Content-Type: application/json")
	Call<String> CreateAWS_SQS(@Header("Authorization") String accessToken, @Path("master_account_id") String master_account_ID, @Body String body);
		
}
