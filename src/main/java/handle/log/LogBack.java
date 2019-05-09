/*package handle.log;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import net.sf.json.JSONObject;

import com.sampullara.cli.Args;
import com.sampullara.cli.Argument;


public class LogBack {
	
	private static final Logger logger = LoggerFactory.getLogger(LogBack.class);
	
	private static final DateFormat dateFormat = new SimpleDateFormat("yyyyMMdd");
	private static String filePrefix = dateFormat.format(Calendar.getInstance().getTime());
	
	@Argument(alias = "h", description = "CDAP master server")
	private static String host = "localhost";
	
	@Argument(alias = "p", description = "CDAP port number")
	private static String port = "11015";
	
	@Argument(alias = "ns", description = "CDAP namespace")
	private static String name_space = "assuredplus";
	
	@Argument(alias = "sn", description = "CDAP stream name")
	private static String stream_name = "pubnubIngress";
	
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

		Args.parse(LogBack.class, args);
		
		createDirectory();
		
		ClientConfig clientConfig = ClientConfig.builder().setConnectionConfig(new ConnectionConfig(host, Integer.parseInt(port), false)).build();
			
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
		StreamClient streamClient = new StreamClient(clientConfig);
		List<StreamEvent> results = new ArrayList<>();
		NamespaceId namespaceId = new NamespaceId(name_space);
		StreamId streamId = namespaceId.stream(stream_name);
		SimpleDateFormat formatter = new SimpleDateFormat("dd-MMM-yyyy HH:mm:ss:SSS");

		try {

			streamClient.getEvents(streamId, start, end, Integer.MAX_VALUE, results);
			logger.info("returned {} events", results.size());
			
			String targetFilePathAndName = directory + File.separator + name_space + "_" + stream_name + "_" + filePrefix + fileExtension;
			String zipFilePathAndName = directory + File.separator + name_space + "_" + stream_name + "_" + filePrefix + ".zip";
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(targetFilePathAndName)));
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
				
				String assuredp_schema = "";
				if(JSONObj.has("assuredp_schema")) {
					assuredp_schema = JSONObj.getString("assuredp_schema");
				}
				
				bw.write(tsStr + "," + formatter.format(ts) + "," + device_id + "," + assuredp_schema + ",\"" + event.replaceAll("\"", "\"\"") + "\"\n");
			}
			
			bw.flush();
			bw.close();
			
			// compressed .csv file to zip
			boolean flag = fileToZip(targetFilePathAndName, zipFilePathAndName);
			if(flag){
				System.out.println("�ļ�����ɹ�!");
			}else{
				System.out.println("�ļ����ʧ��!");
			}
			

		} catch (StreamNotFoundException | UnauthenticatedException | IOException e) {
			e.printStackTrace();
		}	
	}
	
	public static boolean fileToZip(String targetFilePathAndName,String zipFilePathAndName){
		
		boolean flag = false;
		File sourceFile = new File(targetFilePathAndName);
		FileInputStream fis = null;
		BufferedInputStream bis = null;
		FileOutputStream fos = null;
		ZipOutputStream zos = null;
		
		if(sourceFile.exists() == false){
			System.out.println("Target compressed file directory : \"" + targetFilePathAndName + "\" not exist.");
			return flag;
		}
		
		try {
			File zipFile = new File(zipFilePathAndName);
			if(zipFile.exists()){
				zipFile.delete();
				// add a log output
			}

			fos = new FileOutputStream(zipFile);
			zos = new ZipOutputStream(new BufferedOutputStream(fos));
			byte[] bufs = new byte[1024*10];

			// Create zip entry and add source file into the zip package
			ZipEntry zipEntry = new ZipEntry(sourceFile.getName());
			zos.putNextEntry(zipEntry);
			
			// Read source file and write it into the zip package
			fis = new FileInputStream(sourceFile);
			bis = new BufferedInputStream(fis, 1024*10);
			
			int read = 0;
			while((read=bis.read(bufs, 0, 1024*10)) != -1){
				zos.write(bufs,0,read);
			}
			
			flag = true;

		} catch (FileNotFoundException e) {
			e.printStackTrace();
			throw new RuntimeException(e);
		} catch (IOException e) {
			e.printStackTrace();
			throw new RuntimeException(e);
		} finally{
			// Close the stream
			try {
				if(null != bis) bis.close();
				if(null != zos) zos.close();
			} catch (IOException e) {
				e.printStackTrace();
				throw new RuntimeException(e);
			}
		}
		
		// if zip success, then delete the source file
		if(flag) {
			sourceFile.delete();
		}
		
		return flag;
	}
	
}
*/