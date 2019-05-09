package handle.argument;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import net.sf.json.JSONObject;

import com.sampullara.cli.Args;
import com.sampullara.cli.Argument;


/*<!-- com.sampullara.cli.Argument -->
<dependency>
	<groupId>com.github.spullara.cli-parser</groupId>
	<artifactId>cli-parser</artifactId>
	<version>1.1</version>
</dependency>*/

public class TestArgument {
	
	private static final Logger logger = LoggerFactory.getLogger(TestArgument.class);
	
	private static final DateFormat dateFormat = new SimpleDateFormat("yyyyMMdd");
	private static String filePrefix = dateFormat.format(Calendar.getInstance().getTime());
	
	@Argument(alias = "h", description = "CDAP master server")
	private static String host = "localhost";
	
	@Argument(alias = "s", description = "start time minus. default -1 that means end date -1 with 0 HOUR 0 MINUTE 0 SECOND 0 MILLISECOND")
	private static String sMinus = "-1";
	
	@Argument(alias = "e", description = "end time minus. default 0 that means current date with 0 HOUR 0 MINUTE 0 SECOND 0 MILLISECOND")
	private static String eMinus = "0";
	
	@Argument(alias = "d", description = "Data storage directory�� default ��//data")
	private static String directory = "data";
	
	@Argument(alias = "fe", description = "data file extension. default .csv")
	private static String fileExtension = ".csv";

	private static void createDirectory() {
		File dir = new File(directory);
		if(!dir.exists()) {
			dir.mkdirs();
		}
	}
	
	public static void main(String [] args) {
		
		Args.parse(TestArgument.class, args);
		
		createDirectory();
		
//		ClientConfig clientConfig = ClientConfig.builder().setConnectionConfig(new ConnectionConfig(host, 11015, false)).build();
			
    	Calendar calendar = Calendar.getInstance();
    	calendar.set(Calendar.HOUR_OF_DAY, 0);
    	calendar.set(Calendar.MINUTE, 0);
    	calendar.set(Calendar.SECOND, 0);
    	calendar.set(Calendar.MILLISECOND, 0);

    	calendar.add(Calendar.DATE, Integer.parseInt(eMinus));
    	long end = calendar.getTimeInMillis();
    	
    	calendar.add(Calendar.DATE, Integer.parseInt(sMinus));
    	long start = calendar.getTimeInMillis();
    	
		// Construct the client used to interact with CDAP
//		StreamClient streamClient = new StreamClient(clientConfig);
//		List<StreamEvent> results = new ArrayList<>();
//		NamespaceId namespaceId = new NamespaceId("assuredplus");
//		StreamId streamId = namespaceId.stream("pubnubIngress");
		SimpleDateFormat formatter = new SimpleDateFormat("dd-MMM-yyyy HH:mm:ss:SSS");

/*		try {

			streamClient.getEvents(streamId, start, end, Integer.MAX_VALUE, results);
			logger.info("returned {} events", results.size());
			
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(directory + File.separator + filePrefix + fileExtension)));
			bw.write("TIMESTRAMP,TIMELINE,DEVICE_ID,ASSUREDP_SCHEMA,STREAM_EVENT\n");

			for(StreamEvent rst : results) {
				Long ts = rst.getTimestamp();
				String tsStr = String.valueOf(ts);
				String event =new String(rst.getBody().array());
				String newEvent = event.replaceAll("\\\\\"", "");
				JSONObject JSONObj = new JSONObject().fromObject(newEvent);
				
				String device_id = "";
				if(JSONObj.has("device_id")) {
					device_id = JSONObj.getString("device_id");
				} else if (JSONObj.has("deviceID")) {
					device_id = JSONObj.getString("deviceID");
				} else if (JSONObj.has("DeviceID")) {
					device_id = JSONObj.getString("DeviceID");
				}
				
				String assuredp_schema = JSONObj.getString("assuredp_schema");
				
				bw.write(tsStr + "," + formatter.format(ts) + "," + device_id + "," + assuredp_schema + ",\"" + event.replaceAll("\"", "\"\"") + "\"\n");
			}
			
			bw.flush();
			bw.close();

		} catch (StreamNotFoundException | UnauthenticatedException | IOException e) {
			e.printStackTrace();
		}	*/
	}	
}