

# 准备mysql.8.0的docker镜像安装mysql

```bash
mkdir -p /data1/docker_mysql

mkdir -p /data1/docker_mysql/conf

mkdir -p /data1/docker_mysql/logs

mkdir -p /data1/docker_mysql/data

docker run --net host --name mysql -v /data1/docker_mysql/conf:/etc/mysql/conf.d -v /data1/docker_mysql/logs:/logs -v /data1/docker_mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:8.0

# 进⼊入docker镜像

docker exec -it mysql bash

mysql -hlocalhost -P3306 -uroot -p123456

# 修改root⽤用户的登录的密码

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'NLP@kg123';

# 切换到mysql这个database

use mysql
```



# 部署hadoop

```shell
mkdir -p /data1/hadoop-2.9.2/data/tmp
mkdir -p /data1/hadoop-2.9.2/data/var
mkdir -p /data1/hadoop-2.9.2/data/dfs/nn
mkdir -p /data1/hadoop-2.9.2/data/dfs/data

vi /data1/hadoop-2.9.2/etc/hadoop/core-site.xml

<configuration>
        <!-- 指定HDFS中NameNode的地址 -->
        <property>
                <name>fs.defaultFS</name>
                <value>hdfs://9.134.76.122:9000</value>
        </property>
        <!-- 指定hadoop运⾏行行时产⽣生⽂文件的存储⽬目录 /opt/hadoop-2.7.6/data/tmp/ ⽬目录 -->
        <property>
                <name>hadoop.tmp.dir</name>
                <value>file:///data1/hadoop-2.9.2/data/tmp</value>
        </property>
</configuration>

vi /data1/hadoop-2.9.2/etc/hadoop/hadoop-env.sh

# The java implementation to use.
export JAVA_HOME=/data1/TencentKona-8.0.0-232
export HADOOP_HOME=/data1/hadoop-2.9.2/
export HADOOP_SSH_OPTS="-p 36000"


vi /data1/hadoop-2.9.2/etc/hadoop/hdfs-site.xml

<configuration>
	<!-- 设置dfs副本数，不不设置默认是3个 -->
	<property>
		<name>dfs.replication</name>
		<value>2</value>
	</property>
	<!-- 设置secondname的端⼝口 -->
	<property>
		<name>dfs.namenode.secondary.http-address</name>
		<value>master:50090</value>
	</property>
	<property>
		<name>dfs.namenode.name.dir</name>
		<value>file:///data1/hadoop-2.9.2/data/dfs/nn</value>
	</property>
	<property>
		<name>dfs.datanode.data.dir</name>
		<value>file:///data1/hadoop-2.9.2/data/dfs/data</value>
	</property>
	<property>
		<name>dfs.namenode.http-address</name>
		<value>master:50070</value>
	</property>
	 <property>
		<name>dfs.datanode.du.reserved</name>
		<!-- cluster variant -->
		<value>10737418240</value>
    </property>
</configuration>


vi /data1/hadoop-2.9.2/etc/hadoop/slaves
9.134.76.122

vi /data1/hadoop-2.9.2/etc/hadoop/mapred-env.sh
export JAVA_HOME=/data1/TencentKona-8.0.0-232


cp /data1/hadoop-2.9.2/etc/hadoop/mapred-site.xml.template /data1/hadoop-2.9.2/etc/hadoop/mapred-site.xml
vi /data1/hadoop-2.9.2/etc/hadoop/mapred-site.xml

<configuration>
  <!-- 指定mr运行在yarn上 -->
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapred.job.tracker</name>
    <value>master:49001</value>
  </property>
  <property>
    <name>mapred.local.dir</name>
    <value>file:///data1/hadoop-2.9.2/data/var</value>
  </property>
</configuration>


vi /data1/hadoop-2.9.2/etc/hadoop/yarn-env.sh
export JAVA_HOME=/data1/TencentKona-8.0.0-232

vi /data1/hadoop-2.9.2/etc/hadoop/yarn-site.xml
<configuration>
	<!-- reducer获取数据的方式 -->
	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
	<!-- 指定YARN的ResourceManager的地址 -->
	<property>
		<name>yarn.resourcemanager.hostname</name>
		<value>master</value>
	</property>
	<property>
		<name>yarn.scheduler.minimum-allocation-mb</name>
		<value>1024</value>
	</property>
	<property>
		<name>yarn.scheduler.maximum-allocation-mb</name>
		<value>8192</value>
	</property>
	<property>
		<name>yarn.scheduler.minimum-allocation-vcores</name>
		<value>1</value>
	</property>
	<property>
		<name>yarn.scheduler.maximum-allocation-vcores</name>
		<value>4</value>
	</property>
	<property>
	    <name>yarn.resourcemanager.webapp.address.rm1</name>
	    <value>master</value>
	</property>
	<property>
	    <name>yarn.resourcemanager.scheduler.address.rm2</name>
	    <value>master</value>
	</property>
	<property>
	    <name>yarn.resourcemanager.webapp.address.rm2</name>
	    <value>master</value>
	</property>
	<property>
	<name>yarn.nodemanager.resource.memory-mb</name>
	<value>8192</value>
	</property>
</configuration>

vi /etc/profile
# set hadoop environment
export  HADOOP_HOME=/data1/hadoop-2.9.2
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin


iptables -I INPUT -p tcp --dport 8088 -j DROP # 禁⽌止全部访问9200
iptables -I INPUT -s 9.134.76.122 -p tcp --dport 8088 -j ACCEPT # 开启
master节点访问权限

hdfs namenode -format
start-dfs.sh

hadoop fs -mkdir /tmp
hadoop fs -mkdir /history
hadoop fs -put test.txt /tmp


start-yarn.sh

hadoop jar /data1/hadoop-2.9.2/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.2.jar wordcount hdfs://master:9000/tmp/test.txt hdfs://master:9000/out
```



# 部署hive

#### 下载安装包

wget https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-2.3.7/apache-hive-2.3.7-bin.tar.gz

#### 解压以及安装

```shell
mv apache-hive-2.3.6-bin.tar.gz /data1/
cd /data1
tar -zxvf /var/ftp/pub/apache-hive-2.3.7-bin.tar.gz
mv apache-hive-2.3.7-bin/ apache-hive-2.3.7/
```

#### hive mysql配置信息

```xml
cd /data1/apache-hive-2.3.7/conf/
cp hive-log4j2.properties.template hive-log4j2.properties
vi hive-site.xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://192.168.107.144:3306/hive?createDatabaseIfNotExist=true</value>
　</property>
　<property>
    <name>javax.jdo.option.ConnectionDriverName</name>
　　<value>com.mysql.jdbc.Driver</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>root</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>abc123</value>
  </property>
</configuration>
```

#### 依赖下载

下载并拷贝protobuf-java-3.6.1.jar和mysql-connector-java-8.0.17.jar到$HIVE_HOME/lib目录下，删除已有的protobuf-java-2.5.0.jar文件。统一hive和mysql服务的时区。

#### 时区修改

```shell
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime // hive和mysql服务器都要执行，mysql要重启服务
cd /usr/local/apache-hive-2.3.6/bin/
schematool -dbType mysql -initSchema
```

#### 使用hiveserver2和beeline

修改$HADOOP_HOME/etc/hadoop/core-site.xml文件，增加如下配置：

```xml
  <property>
    <name>hadoop.proxyuser.root.hosts</name>
    <value>*</value>
  </property>
  <property>
    <name>hadoop.proxyuser.root.groups</name>
    <value>*</value>
  </property>
```

启动hiverserver2

```shell
cd /data1/apache-hive-2.3.7/bin/
hiveserver2
hiveserver2 & // 以后台形式运行
```

