package handle.cache;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

import com.google.common.cache.CacheBuilder;
import com.google.common.cache.CacheLoader;
import com.google.common.cache.LoadingCache;

public class testGoogleCache {
	
	private static LoadingCache<String,String> schema_cache;
	
	public static void main(String args[]) throws ExecutionException {
		
		
		// initial the cache
		schema_cache = CacheBuilder.newBuilder()
			      .expireAfterWrite(Property.CatchUpdateTime, TimeUnit.SECONDS)
			      .build(new CacheLoader<String,String>() {
			        @Override
			        public String load(String msgType) throws Exception {
			        	return getMessageSchema(msgType);
			        }
			      });
		
		String value = schema_cache.get("key");
		
		if(value == null || value.isEmpty()){
			value = getMessageSchema("key");
			if(value!=null&&(!value.isEmpty())){
				schema_cache.put("key", value);
			}
		}
	}
	
	public static String getMessageSchema(String key) {
		return "query the value from database by key";
	}
	
}
