/*

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

public class GroupOrderByMap {
	private static final Logger logger = LoggerFactory.getLogger(GroupOrderByMap.class);
	
	private static final DateFormat dateFormat = new SimpleDateFormat("yyyyMMdd");
	
	private static final String directory = "data";
	private static final String fileExtension = ".csv";
	private static String filePrefix = dateFormat.format(Calendar.getInstance().getTime());

	private static void createDirectory() {
		File dir = new File(directory);
		if(!dir.exists()) {
			dir.mkdirs();
		}
	}
	
	public static void main(String [] args) {
		
		createDirectory();
		
		ClientConfig clientConfig = ClientConfig.builder().setConnectionConfig(new ConnectionConfig("localhost", 11015, false)).build();
			
    	Calendar calendar = Calendar.getInstance();
    	calendar.set(Calendar.HOUR_OF_DAY, 0);
    	calendar.set(Calendar.MINUTE, 0);
    	calendar.set(Calendar.SECOND, 0);
    	calendar.set(Calendar.MILLISECOND, 0);

    	calendar.add(Calendar.DATE, 0);
    	long end = calendar.getTimeInMillis();
    	
    	calendar.add(Calendar.DATE, -1);
    	long start = calendar.getTimeInMillis();
    	
		// Construct the client used to interact with CDAP
		StreamClient streamClient = new StreamClient(clientConfig);
		List<StreamEvent> results = new ArrayList<>();
		NamespaceId namespaceId = new NamespaceId("assuredplus");
		StreamId streamId = namespaceId.stream("pubnubIngress");
		SimpleDateFormat formatter = new SimpleDateFormat("dd-MMM-yyyy HH:mm:ss:SSS");

		try {

			streamClient.getEvents(streamId, start, end, Integer.MAX_VALUE, results);
			logger.info("returned {} events", results.size());
			
			Map<String, Map<String, List<TimeEvent>>> m1 = new HashMap<String, Map<String, List<TimeEvent>>>();
			Map<String, List<TimeEvent>> m2;
			List<TimeEvent> al3;
			
			List<TimeEvent> listTE = new ArrayList<TimeEvent> ();
			
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(directory + File.separator + filePrefix + fileExtension)));
			bw.write("TIMESTRAMP,TIMELINE,DEVICE_ID,ASSUREDP_SCHEMA,STREAM_EVENT\n");
			
//			Iterator<StreamEvent> rstIt = results.iterator();
//			while(rstIt.hasNext()) {
			for(StreamEvent rst : results) {
//				StreamEvent se = (StreamEvent)rstIt.next();
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
				
				if(device_id.substring(0, 11) == "HealthCheck" || device_id.substring(0, 11).equals("HealthCheck")) {
					listTE.add(new TimeEvent(ts, event));
		            Collections.sort(listTE, new Comparator<TimeEvent>() {
		                @Override
		                public int compare(TimeEvent te1, TimeEvent te2) {
		                    return te1.getTimeStamp().compareTo(te2.getTimeStamp());
		                }
		            });
		            continue;
				}
				
				// group sort / group by device_id, assuredp_schema order by timestamp
				m2 = m1.get(device_id);
	            if(m2 == null){
	            	m2 = new HashMap<String, List<TimeEvent>>();
	            }
	            
				al3 = m2.get(assuredp_schema);
	            if(al3 == null){
	            	al3 = new ArrayList<TimeEvent>();
	            }
	            
	            
	            al3.add(new TimeEvent(ts, event));

	            Collections.sort(al3, new Comparator<TimeEvent>() {
	                @Override
	                public int compare(TimeEvent te1, TimeEvent te2) {
	                    return te1.getTimeStamp().compareTo(te2.getTimeStamp());
	                }
	            });
				
				m2.put(assuredp_schema, al3);
				m1.put(device_id, m2);
			}
			
			
//			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(directory + File.separator + filePrefix + fileExtension)));
//			bw.write("[\n");
//			bw.write("DEVICE_ID,ASSUREDP_SCHEMA,TIMESTRAMP,STREAM_EVENT\n");
//	        for(TimeEvent te : listTE) {
//	        	bw.write("{\"device_id\" : \"HealthCheck\", \"assuredp_schema\" : \"samsung.gears3.alldata.1500994669\", \"timestamp\" : \"" + formatter.format(te.getTimeStamp()) + "\", \"event\" : " + te.getEvent() + "}\n");
//	        }
			
	        for(Map.Entry<String, Map<String, List<TimeEvent>>> m1Entry : m1.entrySet()){
	            for(Map.Entry<String, List<TimeEvent>> m2Entry : m1Entry.getValue().entrySet()){
	            	for(TimeEvent te : m2Entry.getValue()) {
//	            		bw.write("{\"device_id\" : \"" + m1Entry.getKey() + "\", \"assuredp_schema\" : \"" + m2Entry.getKey() + "\", \"timestamp\" : \"" + formatter.format(te.getTimeStamp()) + "\", \"event\" : " + te.getEvent() + "}\n");
	            		bw.write(m1Entry.getKey() + "," + m2Entry.getKey() + "," + formatter.format(te.getTimeStamp()) + ",\"" + te.getEvent().replaceAll("\"", "\"\"") + "\"\n");
//	            	Iterator<TimeEvent> al3It = m2Entry.getValue().iterator();
//	                while(al3It.hasNext()) {
//	        			bw.write(str + "\n");
//	                	TimeEvent te = al3It.next();;
//	        			if(al3It.hasNext()) {
//	        				System.out.println(JSONObj.toString());
//	        				System.out.println(JSONObj.getString("assuredp_schema"));
//	        				bw.write("{\"timestamp\":\"" + formatter.format(se.getTimestamp())+ "\", \"event\":" + str+"},\n");
	        			
//	        			} else {
//	        				bw.write("{\"timestamp\" : \"" + formatter.format(te.getTimeStamp()) + "\", \"device_id\" : \"" + m1Entry.getKey() + "\", \"assuredp_schema\" : \"" + m2Entry.getKey() + "\", \"event\" : " + te.getEvent() + "}\n]");
//	        			}
	                }
	            }
	        }

	        
			bw.flush();
			bw.close();

		} catch (StreamNotFoundException | UnauthenticatedException | IOException e) {
			e.printStackTrace();
		}	
	}	
}

class TimeEvent {
	
	Long timeStamp;
	String event;
	
	public TimeEvent () {}
	
	public TimeEvent (Long timeStamp, String event) {
		super();
		this.timeStamp = timeStamp;
		this.event = event;
	}

	public Long getTimeStamp() {
		return timeStamp;
	}

	public void setTimeStamp(Long timeStamp) {
		this.timeStamp = timeStamp;
	}

	public String getEvent() {
		return event;
	}

	public void setEvent(String event) {
		this.event = event;
	}
	
}*/