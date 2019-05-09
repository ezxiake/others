package handle.cassandra;

import java.io.File;
import java.security.KeyStore;
import java.security.SecureRandom;
import java.util.Optional;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.ColumnDefinitions.Definition;
import com.datastax.driver.core.HostDistance;
import com.datastax.driver.core.PoolingOptions;
import com.datastax.driver.core.ProtocolVersion;
import com.datastax.driver.core.RemoteEndpointAwareJdkSSLOptions;
import com.datastax.driver.core.RemoteEndpointAwareNettySSLOptions;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.SSLOptions;
import com.datastax.driver.core.Session;
import static io.netty.handler.ssl.SslProvider.OPENSSL;


import io.netty.handler.ssl.SslContextBuilder;

public class CassandraTest {

	public Cluster cluster;

	public Session session;

	public void connect() {
		
		try {
		    PoolingOptions poolingOptions = new PoolingOptions();
		    // 每个连接的最大请求数 2.0的驱动好像没有这个方法
		    poolingOptions.setMaxRequestsPerConnection(HostDistance.LOCAL, 32);
		    // 表示和集群里的机器至少有2个连接 最多有4个连接
		    poolingOptions.setCoreConnectionsPerHost(HostDistance.LOCAL, 2).setMaxConnectionsPerHost(HostDistance.LOCAL, 4)
		            .setCoreConnectionsPerHost(HostDistance.REMOTE, 2).setMaxConnectionsPerHost(HostDistance.REMOTE, 4);

		    
			TrustManagerFactory tmf = null;
			KeyStore ks_ts = KeyStore.getInstance("JKS");
			
			ks_ts.load(this.getClass().getResourceAsStream(
					"C:\\workspace\\github-projects\\my_java\\src\\main\\java\\handle\\cassandra\\server-truststore.jks"), // DEFAULT_CLIENT_TRUSTSTORE_PATH
					"ericsson".toCharArray()); // DEFAULT_CLIENT_TRUSTSTORE_PASSWORD

			tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
			tmf.init(ks_ts);

/*			KeyManagerFactory kmf = null;
			KeyStore ks_ks = KeyStore.getInstance("JKS");
			ks_ks.load(this.getClass().getResourceAsStream(
					"C:\\\\workspace\\\\github-projects\\\\my_java\\\\src\\\\main\\\\java\\\\handle\\\\cassandra\\server-keystore.jks"),
					"ericsson".toCharArray()); // CCMBridge.DEFAULT_CLIENT_KEYSTORE_PASSWORD

			kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
			kmf.init(ks_ks, "ericsson".toCharArray()); // DEFAULT_CLIENT_KEYSTORE_PASSWORD

			SSLContext sslContext = SSLContext.getInstance("TLS");
			sslContext.init(kmf != null ? kmf.getKeyManagers() : null, tmf != null ? tmf.getTrustManagers() : null,
					new SecureRandom());

			SSLOptions sslOptions = RemoteEndpointAwareJdkSSLOptions.builder().withSSLContext(sslContext).build();*/
		    
			// ----------------------------------------------------------------------------------
	        SslContextBuilder builder = SslContextBuilder.forClient().sslProvider(OPENSSL).trustManager(tmf);
	        
	        // DEFAULT_CLIENT_CERT_CHAIN_FILE
	        // DEFAULT_CLIENT_PRIVATE_KEY_FILE
	        File certPem = new File("C:\\\\workspace\\\\github-projects\\\\my_java\\\\src\\\\main\\\\java\\\\handle\\\\cassandra\\node0.cer.pem");
	        File keyPem = new File("C:\\\\workspace\\\\github-projects\\\\my_java\\\\src\\\\main\\\\java\\\\handle\\\\cassandra\\node0.key.pem");
	        builder.keyManager(certPem, keyPem);
			SSLOptions sslOptions =  new RemoteEndpointAwareNettySSLOptions(builder.build());
			// ----------------------------------------------------------------------------------
		    
		    // addContactPoints:cassandra节点ip withPort:cassandra节点端口 默认9042
		    // withCredentials:cassandra用户名密码 如果cassandra.yaml里authenticator：AllowAllAuthenticator 可以不用配置
		    cluster = Cluster.builder().addContactPoints("34.217.70.75").withPort(9042)
		    		.withSSL(sslOptions).withProtocolVersion(ProtocolVersion.V4)
//		            .withCredentials("cassandra", "cassandra").withSSL(sslOptions).withPoolingOptions(poolingOptions).build();
		    .withCredentials("test", "test").withPoolingOptions(poolingOptions).build();
		    // 建立连接
		    // session = cluster.connect("test");连接已存在的键空间
		    session = cluster.connect("mydb");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * 创建键空间
	 */
	public void createKeyspace()
	{
	    // 单数据中心 复制策略 ：1
	    String cql = "CREATE KEYSPACE if not exists mydb WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}";
	    session.execute(cql);
	}

	/**
	 * 创建表
	 */
	public void createTable()
	{
	    // a,b为复合主键 a：分区键，b：集群键
	    String cql = "CREATE TABLE if not exists mydb.test (a text,b int,c text,d int,PRIMARY KEY (a, b))";
	    session.execute(cql);
	}
	
	/**
	 * 插入
	 */
	public void insert()
	{
	    String cql = "INSERT INTO mydb.test (a , b , c , d ) VALUES ( 'a2',4,'c2',6);";
	    session.execute(cql);
	}

	/**
	 * 修改
	 */
	public void update()
	{
	    // a,b是复合主键 所以条件都要带上，少一个都会报错，而且update不能修改主键的值，这应该和cassandra的存储方式有关
	    String cql = "UPDATE mydb.test SET d = 1234 WHERE a='aa' and b=2;";
	    // 也可以这样 cassandra插入的数据如果主键已经存在，其实就是更新操作
	    String cql2 = "INSERT INTO mydb.test (a,b,d) VALUES ( 'aa',2,1234);";
	    // cql 和 cql2 的执行效果其实是一样的
	    session.execute(cql);
	}

	/**
	 * 删除
	 */
	public void delete()
	{
	    // 删除一条记录里的单个字段 只能删除非主键，且要带上主键条件
	    String cql = "DELETE d FROM mydb.test WHERE a='aa' AND b=2;";
	    // 删除一张表里的一条或多条记录 条件里必须带上分区键
	    String cql2 = "DELETE FROM mydb.test WHERE a='aa';";
	    session.execute(cql);
	    session.execute(cql2);
	}

	/**
	 * 查询
	 */
	public void query()
	{
	    String cql = "SELECT * FROM mydb.test;";
	    String cql2 = "SELECT a,b,c,d FROM mydb.test;";

	    ResultSet resultSet = session.execute(cql);
	    System.out.print("this is the column name : ");
	    for (Definition definition : resultSet.getColumnDefinitions())
	    {
	        System.out.print(definition.getName() + " ");
	    }
	    System.out.println();
	    System.out.println(String.format("%s\t%s\t%s\t%s\t\n%s", "a", "b", "c", "d",
	            "--------------------------------------------------------------------------"));
	    for (Row row : resultSet)
	    {
	        System.out.println(String.format("%s\t%d\t%s\t%d\t", row.getString("a"), row.getInt("b"),
	                row.getString("c"), row.getInt("d")));
	    }
	}
	
	public static void main(String args[]) {
		CassandraTest ct = new CassandraTest();
		ct.connect();
//		ct.createKeyspace();
//		ct.createTable();
//		ct.insert();
//		ct.update();
//		ct.query();
		
		
		
		
	}
}
