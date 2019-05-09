# cassandra cluster auto-installation with Ansible

## Limitation
The documents only work and tested on AWS Ubuntu system, all other Cloud system and OS not support now.

## System Requirement
<ul>
<li>one Ubuntu system need as the manager node. The system shall reach to AWS instance, AWS and the network shall stable enough to avoid install issues. </li>
<li>user shall have basic Linux command skill and basic script writing skill.  </li>
<li>To create AWS instance automatically, User need the AWS access key and AWS secret key (<a href="#">how to get the keys</a>)</li>
<li>the ansible manager node shall has the passwordless connection to others nodes </li>
</ul>

## Software Requirement
<table>
<tr>
<td>Software</td>
<td>Version</td>
<td>Description</td>
</tr>
<tr>
<td>Ubuntu OS</td>
<td>14.4</td>
<td></td>
</tr>
<tr>
<td>Python</td>
<td>2.6 or 2.7</td>
<td></td>
</tr>
<tr>
<td>Ansible</td>
<td>2.3.0.0 (current latest release version)</td>
<td></td>
</tr>
</table>

## To quick start
<li>Login to the ansible server with ubuntu user(Oregon - 52.43.241.146; Singapore - 54.254.180.92)</li>

```
$ cd /home/ubuntu/
$ git clone "https://github.com/AssuredProject/cassandra_auto_deploy.git" "./cassandra_auto_deploy"
```

## Update configurations
```
$ vim /home/ubuntu/cassandra_auto_deploy/group_vars/all
```

|Parameter name|Parameter values(e.g.)|Description|
|:---|:---|:---|
|CLUSTER_NAME|cassandra_cluster|Set the cluster name|
|ANSIBLE_SECURITY_IP|172.31.29.69/32|Set the manager node private ip/32|
|region|us-west-2|us-west-1(N.California)/us-west-2(Oregon)/ap-southeast-1(Singapore)|
|zone|us-west-2b|A AWS zone|
|aws_cluster_count|3|The number of cluster members|
|aws_cluster_type|m4.2xlarge|The type of cluster members|
|cluster_volumes||The volume of cluster members|
|vpc_id|vpc-8ffb0ce8|this one for us-west-2 region(Oregon)|
|vpc_subnet|subnet-75ffec11|this one for us-west-2 region(Oregon)|
|image|ami-8f78c2f7|ubuntu 14.4 us-west-2b(Oregon)|

<li>Change the script file authority</li>

```
$ sudo chmod 777 /home/ubuntu/cassandra_auto_deploy/startup.sh
```

<li>Run the script</li>

```
$ /home/ubuntu/cassandra_auto_deploy/startup.sh
```

## How to get the ssl java keystore file(CERTIFICATE)

<li>Login to the ansible server with ubuntu user(Oregon - 52.43.241.146; Singapore - 54.254.180.92)</li>

```
$ cd /home/ubuntu/cassandra_auto_deploy/security
```
You can see the CERTIFICATE files like `cassandra.keystore.{private ip}.jks`.</br>
Each cassandra node has a corresponding certificate, they are different, but they are transparent to the client.</br>
So the client can use any certificate to access any cassandra node.</br>

<li>The certificate is valid for 365 days.</li>
<li>SSL KEYSTORE PASSWORD is `ericsson`</li>
<li>SSL TRUSTSTORE PASSWORD  is `ericsson`</li></br>

<li>Java cassandra Consumer SSL Demo</li>
https://github.com/AssuredProject/cassandra_auto_deploy/blob/master/demo/Consumer_SSL_Demo.java </br>

<li>Java cassandra Producer SSL Demo</li>
https://github.com/AssuredProject/cassandra_auto_deploy/blob/master/demo/Producer_SSL_Demo.java

## How to create a certificate manually if the certificate is expired
<li>At every node - pre-condition</li>

```
$ cd /opt/cassandra/conf
```

<li>At some node - Createing your own CA</li>

It will sign all certificates in the cluster with a single CA.</br>
It will be copied to other nodes to be used for sign certificate.</br>

```
$ printf "er\nericsson\nericsson\nericsson\nericsson\nericsson\nericsson@ericsson.com\n" | openssl req -new -x509 -keyout ca-key -out ca-cert -days 365 -passout pass:ericsson
```
then copy `ca-key` and `ca-cert` to other clusters. The parameter `-days 365` means the certificate is valid for 365 days.</br>

<li>At every node - Generate the key into a keystore initially so that we can export and sign it later with CA.</li>

```
$ printf "ericsson\nericsson\nericsson\nericsson\nericsson\nericsson\nericsson\nericsson\nyes\n\n" | keytool -keystore .keystore -alias localhost -validity 365 -genkey -keyalg RSA
```
The parameter `-days 365` means the certificate is valid for 365 days.</br>

<li>At every node - Export the certificate from the keystore</li>

```
$ printf "ericsson\n" | keytool -keystore .keystore -alias localhost -certreq -file cert-file
```

<li>At every node - Then sign it with the CA</li>

```
$ openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:ericsson
```

The parameter `-days 365` means the certificate is valid for 365 days.</br>

<li>At every node - Import both the certificate of the CA and the signed certificate into the keystore</li>

```
$ printf "ericsson\nyes\n" | keytool -keystore .keystore -alias CARoot -import -file ca-cert
$ printf "ericsson\nyes\n" | keytool -keystore .keystore -alias localhost -import -file cert-signed
```

Then you can get the `.keystore` CERTIFICATE filea from each node</br>

## If you need to install the Ansible
<li>Login to the manager node, here we use one AWS instance for example.</li>  
<li>Use apt to install ansible:</li>

```
$ sudo apt-get install software-properties-common
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get install ansible
```

<li>Make sure the ansible be ready:</li>

```
$ ansible --version  
```
ansible 2.3.0.0  






