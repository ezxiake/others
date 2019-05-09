package handle.kafka;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRebalanceListener;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.config.SslConfigs;
 
import java.util.Collection;
import java.util.Collections;
import java.util.Properties;

public class Consumer_SASL_SSL_Demo {
	public static void main(String[] args) {
		   
//		System.setProperty("java.security.auth.login.config", "C:\\workspace\\github-projects\\my_java\\src\\main\\java\\handle\\kafka\\kafka_client_jaas.conf");
		   
		Properties consumerProps = new Properties();
		consumerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "54.184.71.206:9093,34.217.101.251:9093,18.236.136.176:9093"); // test
//		consumerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "54.184.84.94:9093,34.210.154.205:9093,34.216.247.239:9093"); // tmp
		
//		for SASL
//		consumerProps.setProperty ("sasl.mechanism", "PLAIN"); 
		
//		consumerProps.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
		consumerProps.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SSL");
//		consumerProps.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT");
		
//		configure the following three settings for SSL Authentication
		consumerProps.put(SslConfigs.SSL_KEYSTORE_LOCATION_CONFIG, "C:\\workspace\\github-projects\\my_java\\src\\main\\java\\handle\\kafka\\kafka.keystore.172.31.26.202.jks");  
		consumerProps.put(SslConfigs.SSL_KEYSTORE_PASSWORD_CONFIG, "ericsson");
		consumerProps.put(SslConfigs.SSL_KEYSTORE_TYPE_CONFIG, "JKS");
		
//		configure the following four settings for SSL Encryption
		consumerProps.put(SslConfigs.SSL_TRUSTSTORE_LOCATION_CONFIG, "C:\\workspace\\github-projects\\my_java\\src\\main\\java\\handle\\kafka\\kafka.keystore.172.31.31.47.jks");  
		consumerProps.put(SslConfigs.SSL_TRUSTSTORE_PASSWORD_CONFIG, "ericsson");  
		consumerProps.put(SslConfigs.SSL_TRUSTSTORE_TYPE_CONFIG, "JKS");
		consumerProps.put(SslConfigs.SSL_KEY_PASSWORD_CONFIG, "ericsson");  
		
		consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, "my-group");
		consumerProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
		consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
		consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
		
		KafkaConsumer<byte[], byte[]> consumer = new KafkaConsumer<>(consumerProps);
		TestConsumerRebalanceListener rebalanceListener = new TestConsumerRebalanceListener();
		consumer.subscribe(Collections.singletonList("test"), rebalanceListener);
	 
		while (true) {
			ConsumerRecords<byte[], byte[]> records = consumer.poll(1000);
			for (ConsumerRecord<byte[], byte[]> record : records) {
				System.out.printf("Received Message topic =%s, partition =%s, offset = %d, key = %s, value = %s\n", record.topic(), record.partition(), record.offset(), record.key(), record.value());
			}
	 
			consumer.commitSync();
		}
	 
	}
	 
	private static class  TestConsumerRebalanceListener implements ConsumerRebalanceListener {
		@Override
		public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
			System.out.println("Called onPartitionsRevoked with partitions:" + partitions);
		}
 
		@Override
		public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
			System.out.println("Called onPartitionsAssigned with partitions:" + partitions);
		}
	}
	
}



