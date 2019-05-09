package handle.restAPI;

public class RestAPIReponseCode {
	
	// code for oaxis 
	private final static int AccessOaxisCodeBase = 50000;
	public final static int OaxisSuccess = 200;
	public final static int Failure_GetCookie = AccessOaxisCodeBase+1;
	public final static int Failure_GetCode = AccessOaxisCodeBase+2;
	public final static int Failure_GetAccesstoken = AccessOaxisCodeBase+3;
	public final static int Failure_RefreshAccesstoken = AccessOaxisCodeBase+4;
	public final static int Failure_GetMasterInfo = AccessOaxisCodeBase+5;
	public final static int Failure_CreateSubAccount = AccessOaxisCodeBase+6;
	public final static int Failure_ActiveDevice = AccessOaxisCodeBase+7;
	public final static int Failure_DeactiveDevice = AccessOaxisCodeBase+8;
	public final static int Failure_CreateSQS = AccessOaxisCodeBase+9;
	public final static int Failure_GetDeviceConfigInfo = AccessOaxisCodeBase+11;
	
	// code for adatper
	public final static int OaxisAdapterSuccess = 200;
	public final static int OaxisAdapterDataNotFound = 404;
	public final static int InvalidJsonFormat = 400;
	public final static int OaxisAdapterExceptionError = 500;
	public final static int OaxisMissRequiredField = 404;
	public final static int OaxisDeviceAlreadyActive = 401;
	public final static int OaxisMasterEmpty = 405;
	public final static int OaxisMissRequireData = 406;
	public final static int OaxisDatasetError = 407;
	public final static int OaxisResponseInsideCodeUnequal200Error = 408;
	public final static int OaxisSubAccountEmpty = 409;
	public final static int OaxisDeviceNotOnBoard = 404;
	public final static int OaxisAPIInvokeFailure = 402;
}
