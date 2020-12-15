[TOC]
## 简介

 本文主要介绍如何通过镜像部署文档型问答服务，文档型问答服务需要的基础软件包括elasticsearch、redis和mysql，因此，首先需要在本机安装Docker（第1节），然后分别获取elasticsearch、redis和mysql的镜像文件并进行安装（第2节），镜像文件可以从DocHub获取（第2.1节），也可以直接使用我们下载好的镜像文件（第2.2节）

**说明**：docservice.zip中共包含4个镜像文件、1个配置文件和1个语料文件夹:

1. es-ik.tar: elasticsearch-ik镜像文件(安装了IK分词插件)
2. redis.tar: redis镜像文件
3. mysql.tar: mysql镜像文件
4. docqa.tar: 文档型问答服务镜像文件
5. config.yaml: 文档型问答服务配置文件
6. corpus: 156篇文档

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

3. 安装 Docker Engine-Community

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
   $ docker images                     # 显示镜像
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

3. 拉取redis镜像(5.0.7)

   ```
   $ docker pull redis 
   ```

4. 拉取mysql镜像(8.0.18)

   ```
   $  docker pull mysql 
   ```

#### 2.2 直接使用提供的镜像文件

1. 加载elasticsearch-ik(v6.2.4)镜像

   ```
   $ docker load --input es-ik.tar
   ```

2. 加载redis镜像(v5.0.7)

   ```
   $ docker load --input redis.tar
   ```

3. 加载mysql镜像(v8.0.18)

   ```
   $ docker load --input mysql.tar
   ```

### 3. 启动基础软件容器

0. 建立网桥

```
  docker network create --subnet=172.18.0.0/16 my-net
```

1. 启动elasticsearch-ik 

```
   $ mkdir -p /home/docker/es/data  (索引文件存放路径)
   $ chmod 777 -R /home/docker/es/data
   $ mkdir -p /home/docker/es/config/  (配置文件存放路径)
   $ cd /home/docker/es/config/ 编辑es1.yml文件(network.host: 172.18.0.2)
   $ docker run -idt --name es --net my-net --ip 172.18.0.2 \
   -v /home/docker/es/data:/usr/share/elasticsearch/data \
   -v /home/docker/es/config/es1.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
   -e "discovery.type=single-node" bachue/elasticsearch-ik:6.2.4 /usr/local/bin/docker-entrypoint.sh
   # PS: 挂载索引文件和配置文化
```

2. 启动redis

   ```
   $ docker run --name redis --net my-net --ip 172.18.0.3 -d redis --requirepass "sd_Electric2020"
   ```

3. 启动mysql

   ```
   $ docker run --name mysql --net my-net -d --ip 172.18.0.4 \
   -e MYSQL_ROOT_PASSWORD=sd_Electric2020 mysql
   # MYSQL_ROOT_PASSWORD 设置的是mysql的root登录密码
   ```

4. 进入mysql容器，并建立数据库

   ```bashrc
   $ docker exec -it mysql /bin/bash
   $ mysql -u root -p
    > create database docbot;
   ```

### 4. 安装文档型问答服务

1. 加载docqa镜像

   ```
   $ docker load --input docqa.tar
   ```

2. 修改配置文件config.yaml

```
    ESAddress: http://172.18.0.2:9200
    mysql.host: 172.18.0.4
    mysql.database: "docbot"
    mysql.password: "sd_Electric2020"
    redis.port: "172.18.0.3:6379"
    redis.password: "sd_Electric2020"
```

3. 启动容器

```
   $ chmod 777 -R /home/docqa/config.yaml
   $ docker run --name docqa --net my-net --ip 172.18.0.5 \
    -v /home/docqa/corpus:/iask-DocServer/go/corpus \
    -v /home/docqa/log:/iask-DocServer/go/log \
    -v /home/docqa/parselog:/iask-DocServer/java/log \
    -v /home/data/file:/data/file \
    -v /home/docqa/config.yaml:/iask-DocServer/go/config/dev/config.yaml \
    -v /home/docqa/resource:/iask-DocServer/go/resource \
    -v /home/docqa/config/data:/iask-DocServer/go/config/data \
    -d ${IMAGE_NAME}$:${IMAGE_TAG}$
   # PS: ${IMAGE_NAME}$为镜像名称，${IMAGE_TAG}$为镜像版本号
   # /home/docqa/corpus 语料存放路径
   # /home/docqa/log 服务主模块（问答）日志
   # /home/docqa/parselog 文档解析模块日志
   # /home/data/file 与全文检索服务一致
   # /home/docqa/resource license文件存放路径
   # /home/docqa/config/data 服务配置文件
```

4. license校验

   A) 将/home/docqa/resource/applicationCode.pem 文件（申请码）给回项目负责人甲

   B) 由项目负责人甲提供激活码文件（activationCode.txt），将激活码文件放入/home/docqa/resource/文件夹下

   C) docker restart docqa 重启问答引擎

   D) docker logs docqa --since 3m 如果引擎正常运行，则表明license校验成功

### 5. 验证文档型问答服务

0. 数据准备

   /home/docqa/corpus下的数据目录组织

   ```
   /home/docqa/corpus/user1/WORD/1.doc
   /home/docqa/corpus/user1/WORD/2.doc
   /home/docqa/corpus/user2/WORD/3.doc
   /home/docqa/corpus/user2/WORD/4.doc
   ```

1. InitData 文档解析与数据处理 

   ```
   curl -H "Content-Type:application/json" -X POST -d '{}' http://localhost:9101/docbot/FullInitData?ProductId="user1"
   ```

2. GetState 查询任务状态

   ```
   curl -H "Content-Type:application/json" -X POST -d '{}' 
   http://localhost:9101/docbot/GetState?ProductId="user1"
   ```

3. Query 问答接口

   针对1.doc和2.doc提问

   ```
    curl -H "Content-Type:application/json" -X POST 
    -d '{"Query":"问题问题"}' http://localhost:9101/docbot/Query?ProductId="user1"
   ```

### 6. 更新服务

1. 更新问答服务

```
chmod +x iask-DocQA
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
