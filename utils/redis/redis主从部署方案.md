#### 镜像部署

下面以一主一从为例，展开主从部署的实验。

1. 设置指定网络

```
docker network create --subnet=192.168.1.0/24 redis-network
```

2. 运行主从容器

   **主容器**

```
docker run -idt --network=redis-network --ip=192.168.1.2 --name redis-master redis
```

   	**从容器**

```
docker run -idt --network=redis-network --ip=192.168.1.3 --name redis-slave redis
```

3. 主从复制：

   a) 进入从容器

   ```
   docker exec -it redis-slave sh
   ```

   b) 开启主从复制

   ```
   127.0.0.1:6379 > slaveof 192.168.1.2 6379
   127.0.0.1:6379 > info replication
   ```

<img src="	redis-slave.png" style="zoom:45%;" />

4. 测试：

   若想查看主从设置是否生效，可在主机添加数据，再从从机查询，若查询得到，则证明设置成功。

   ![](	redis-master.png)

#### 开启主从复制的三种方法：

a) 修改配置文件

​	在从服务器的配置文件(redis.conf)中加入： slaveof <masterip> <masterport>

​	启动服务时指定配置文件路径 

b) 启动命令

​	redis-server启动命令后加入 --slaveof <masterip> <masterport>

c) 客户端命令

​	redis 服务器启动后，直接通过客户端执行命令：slaveof <masterip> <masterport>  则该redis实例成为从节点

```
# masterauth <master-password>  //设置主机密码
```