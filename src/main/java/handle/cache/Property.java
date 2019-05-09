package handle.cache;

public class Property {
	
	// vendoradapter type
	public static final String VendorType = "Oaxis";
	public static int UserModuleFeedbackRetry = 3;
	
	// app type name and desciption
	public static final String AppName = VendorType+"Adapter";
	public static final String AppDesc = VendorType+" Cloud Adapter";
	
	public static final String UserModuleAppName = "UserModule";
	public static final String UserModuleDeviceServiceName = "UserControllerService";
	
	public static final String OaxisSubscribeWorkerName = VendorType+"SubscribeWorker";
	public static final String OaxisSubscribeWorkerDesc = VendorType+"SubscribeWorker";
	
	// service name
	public static final String AdapterServiceName = VendorType+"AdapterService";
	public static final String AdapterServiceDesc = VendorType+" adapter REST API";	
	
	// watch service name
	public static final String AdapterWatchServiceName = VendorType+"AdapterWatchService";
	public static final String AdapterWatchServiceDesc = VendorType+" adapter Watch REST API";	
	
	// data set name
	public static final String OaxisActiveDeviceDataSetName = VendorType+"OnBoardDeviceDataSet";
	public static final String OaxisActiveDeviceDataSetDesc = "the dataset store all onboarded device info";
	
	public static final String OaxisDeviceIDMappingDataSetName = VendorType+"IDMappingDataSet";
	public static final String OaxisDeviceIDMappingDataSetDesc = "the device id mapping table from device ID to hostUniqueID";
	
	public static final String OaxisMessageTypeSchemaMappingDataSetName = VendorType+"SchemaMappingDataSet";
	public static final String OaxisMessageTypeSchemaMappingDataSetDesc = "the dataset store the oaxis message type and assured+ message type mapping";
	
	public static final String OaxisUserDataSetName = VendorType+"UserInfoDataSet";
	public static final String OaxisUserDataSetDesc = "the dataset store the sub account info";
	
	public static final String OaxisLogDataSetName = VendorType+"LogDataset";
	public static final String OaxisLogDataSetDesc = "the dataset store the device onboard success and failure logs";
	
	//Oaxis Master UserName
	public static final String Oaxis_MasterUser_Key = "MASTERUSER";
	public static final int    Oaxis_updateTokenBeforeDay = 10;
//	public static final String Oaxis_API_BaseURL = "https://api.oaxis.com/watchserver/";
	public static final String Oaxis_API_BaseURL_Production = "https://prod-api.oaxis.com/";
	public static final String Oaxis_API_BaseURL_Stage = "https://staging-api.oaxis.com/";
	public static final String Oaxis_API_BaseURL_Develop = "http://dev-api.oaxis.com/";
	//public static final String Oaxis_aws_sqs_url = "https://sqs.us-west-2.amazonaws.com/052660077578/60515";
	
	public static int CatchUpdateTime = 300;
	
}
