## 简介

​	本文主要介绍如何通过镜像部署文档型问答服务，文档型问答服务需要的基础软件包括elasticsearch、redis和mysql，因此，首先需要在本机安装Docker（第1节），然后分别获取elasticsearch、redis和mysql的镜像文件并进行安装（第2节），镜像文件可以从DocHub获取（第2.1节），也可以直接使用我们下载好的镜像文件（第2.2节）

**说明**：docservice.zip中共包含4个镜像文件、1个配置文件和1个语料文件夹:

1. es-ik.tar: elasticsearch-ik镜像文件(安装了IK分词插件)
2. redis.tar: redis镜像文件
3. mysql.tar: mysql镜像文件
4. docqa.tar: 文档型问答服务镜像文件
5. config.yaml: 文档型问答服务配置文件

### 1. 安装Docker

1. 卸载旧版本

   ```
   $ yum remove docker docker-client docker-client-latest docker-common docker-latest \
               docker-latest-logrotate docker-logrotate docker-engine
   ```

2. 设置Docker仓库,之后从这个仓库安装和更新Docker

   ```bashrc
    $ yum install -y yum-utils device-mapper-persistent-data lvm2
    $ yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   ```

3.  安装 Docker Engine-Community

   ```bashrc
   $ yum install -y docker-ce docker-ce-cli containerd.io
   ```

4. 启动 Docker

   ```bashrc
   $ systemctl start docker
   ```

5. 关闭 Docker

   ```bashrc
   $ systemctl stop docker
   ```

6. 验证 Docker

   ```bashrc
   $ docker pull library/hello-world  # 拉取镜像
   $ docker images									   # 显示镜像
   $ docker run hello-world           # 运行镜像
   ```

### 2. 获取基础软件镜像文件

#### 2.1 DocHub获取镜像文件

1. 注册DocHub账号，并使用账号登录

   ```bashrc
   	$ docker login
   ```

2. 拉取elasticsearch-ik镜像

   ```
   $ docker pull bachue/elasticsearch-ik:6.2.4
   ```

3.  拉取redis镜像(5.0.7)

   ```
   $ docker pull redis 
   ```

4. 拉取mysql镜像(8.0.18)

   ```
   $	docker pull mysql 
   ```

#### 2.2 直接使用提供的镜像文件

1. 加载elasticsearch-ik镜像

   ```
   $ docker load --input es-ik.tar
   ```

2. 加载redis镜像(5.0.7)

   ```
   $ docker load --input redis.tar
   ```

3. 加载mysql镜像(8.0.18)

   ```
   $ docker load --input mysql.tar
   ```

### 3. 启动基础软件容器

1. 启动elasticsearch-ik 
```
   $ mkdir -p /home/docker/es/data
   $ chmod 777 -R /home/docker/es/data
   $ mkdir -p /home/docker/es/config/
   $ cd /home/docker/es/config/ 编辑es1.yml文件(network.host: localhost)
   $ docker run -idt --name es --net host \
   -v /home/docker/es/data:/usr/share/elasticsearch/data \
   -v //home/docker/es/config/es1.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
   -e "discovery.type=single-node" bachue/elasticsearch-ik:6.2.4 /usr/local/bin/docker-entrypoint.sh
```
2. 启动redis

   ```
   $ docker run --name redis --net host -d redis --requirepass "sd_Electric2020"
   ```

3. 启动mysql

   ```
   $ docker run --name mysql --net host -d \
   -e MYSQL_ROOT_PASSWORD=sd_Electric2020 mysql
   # MYSQL_ROOT_PASSWORD 设置的是mysql的root登录密码
   ```

4. 进入mysql容器，并建立数据库

   ```bashrc
   $ docker exec -it mysql /bin/bash
   $ mysql -u root -p
   	> create database mytest;
   ```

### 4. 安装文档型问答服务

1.  加载docqa镜像

   ```
   $ docker load --input docqa.tar
   ```

2. 启动容器
```
   $ chmod 777 -R /home/docker/docqa/config.yaml
   $ docker run --name docqa --net host \
    -v /home/docker/docqa/corpus:/iask-DocServer/go/corpus \
    -v /home/docker/docqa/log:/iask-DocServer/go/log \
    -v /home/data/file:/data/file \
    -v /home/docker/docqa/config.yaml:/iask-DocServer/go/config/dev/config.yaml \
    -d ccr.ccs.tencentyun.com/iask/shandong_electric_power:44
```

### 5. 验证文档型问答服务

1. InitData 文档解析与数据处理 

   ```
   curl -H "Content-Type:application/json" -X POST -d '{}' http://localhost:9101/docbot/InitData?ProductId="sduser"
   ```

2. GetState 查询任务状态

   ```
   curl -H "Content-Type:application/json" -X POST -d '{}' 
   http://localhost:9101/docbot/GetState?ProductId="sduser"
   ```

3. Query 问答接口
   ```
    curl -H "Content-Type:application/json" -X POST 
    -d '{"Query":"油浸式电力变压器本体的检修要点都有哪些"}' http://localhost:9101/docbot/Query?ProductId="sduser"
   ```

### 6. 更新服务
1. 更新问答服务
```
docker cp iask-DocQA docqa:/iask-DocServer/go/

```
2. 更新文档解析服务
```
docker cp fileparser-1.0-SNAPSHOT.jar docqa:/iask-DocServer/java/

```
3. 重启服务
```
docker restart docqa
```