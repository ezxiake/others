package handle.kafka;

import java.util.Properties;  

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.producer.Callback;
import org.apache.kafka.clients.producer.KafkaProducer;  
import org.apache.kafka.clients.producer.ProducerConfig;  
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.config.SslConfigs;  
  
public class Producer_SASL_SSL_Demo {  
    public static void main(String[] args) {
//    	String fsPath=System.getProperty("user.dir"); 
//    	System.out.println(fsPath);
    	
    	// for SASL
//    	System.setProperty("java.security.auth.login.config", "C:\\workspace\\github-projects\\my_java\\src\\main\\java\\handle\\kafka\\kafka_client_jaas.conf");
    	
		Properties producerProps = new Properties();  
		producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "54.184.71.206:9093,34.217.101.251:9093,18.236.136.176:9093"); // test
//		producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "54.184.84.94:9093,34.210.154.205:9093,34.216.247.239:9093"); // tmp
		 
//		producerProps.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
		producerProps.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SSL");
//		producerProps.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT");
		 
//		for SASL
//		producerProps.setProperty ("sasl.mechanism", "PLAIN"); 
		 
		producerProps.put(ProducerConfig.ACKS_CONFIG, "all");
		producerProps.put(ProducerConfig.RETRIES_CONFIG, 0);
		producerProps.put("batch.size", 16384);
		producerProps.put("linger.ms", 1);
		producerProps.put("buffer.memory", 33554432);
		 
//		producerProps.put(ProducerConfig.CLIENT_ID_CONFIG, "myApiKey");
		
		producerProps.put(SslConfigs.SSL_KEYSTORE_LOCATION_CONFIG, "C:\\workspace\\github-projects\\my_java\\src\\main\\java\\handle\\kafka\\kafka.keystore.172.31.26.202.jks");  
		producerProps.put(SslConfigs.SSL_KEYSTORE_PASSWORD_CONFIG, "ericsson");
		producerProps.put(SslConfigs.SSL_KEYSTORE_TYPE_CONFIG, "JKS");
		producerProps.put(SslConfigs.SSL_TRUSTSTORE_LOCATION_CONFIG, "C:\\workspace\\github-projects\\my_java\\src\\main\\java\\handle\\kafka\\kafka.keystore.172.31.26.202.jks");  
		producerProps.put(SslConfigs.SSL_TRUSTSTORE_PASSWORD_CONFIG, "ericsson");
		producerProps.put(SslConfigs.SSL_TRUSTSTORE_TYPE_CONFIG, "JKS");
		producerProps.put(SslConfigs.SSL_KEY_PASSWORD_CONFIG, "ericsson");  
		
		producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
		producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
		 
		KafkaProducer<String, String> producer = new KafkaProducer<String, String>(producerProps);
		 
		for(int i = 0; i < 1; i++) {
			String key=String.valueOf("key"+i);
			String data="hello kafka message:"+key;
//			producer.send(new ProducerRecord<>("test", key, data), new Callback() {
//				    @Override
//				    public void onCompletion(RecordMetadata recordMetadata, Exception e) {
//				        e.printStackTrace();
//				    }
//			});
			producer.send(new ProducerRecord<>("test", key, data));
		}
		producer.close();
    }  
}


