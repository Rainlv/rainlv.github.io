---
title: Docker基础
date: 2022-04-17 23:17:47 +0800
categories: [工具]
tags: [docker]
---

## 常用命令

![image-20210204164016051](C:\Users\i\AppData\Roaming\Typora\typora-user-images\image-20210204164016051.png)

### 查看信息

```shell
# 查看运行容器
docker ps
	# 参数
	-a 	# 显示所有容器(不论是否在运行)
	-p	# 静默显示，只显示容器ID
```

``` shell
# 查看容器内进程信息
docker top 容器ID
```

```shell
# 查看本地镜像信息
docker images
	# 参数
	-q 	# 静默显示，只显示ID
```

```shell
# 查看容器日志信息(如终端打印信息)
docker logs [Opt] xxx
```

```shell	
# 返回容器详细信息的JSON数据格式
docker inspect 容器ID
```

```shell
# 查看容器内存使用情况
docker stats
```

### 镜像命令

#### 查找搜索

```shell
#从DockerHub上搜索指定镜像名
docker search [Opt] 镜像名
# 常用参数
	-f 过滤
```

#### 添加

```shell
docker pull 镜像名[:标签]  # 所谓标签就是版本号，不加默认latest，即最新版
```

#### 删除

```shell
docker rmi 镜像名[:标签]

# 批量删除
docker rmi $(docker images -q)
```

### 容器命令

#### 运行

```shell
# 运行新容器
docker run 镜像名
	# 参数介绍
	-d   					   # 静默模式，后台运行
    -p(小写) 宿主机端口:容器端口   # 建立宿主机和容器指定端口映射
    -P(大写)  				  # 随机端口映射
    -it  					   # 交互式
    --name  				   # 容器命名
   
# 容器暂停/停止时，重新运行
docker start 容器ID
docker restart 容器ID
```

#### 退出

```shell
# 处于容器终端时
	exit  			# 退出并停止
	Ctrl + P + Q  	# 退出但不停止
	
# 处于宿主机终端时：
	docker stop 容器ID
```

#### 进入

```shell
docker attach 容器ID

docker exec 容器ID
	# 参数
	-it 进入容器获得交互式窗口
```

#### 提交

```shell
docker commit -a 作者 -m 提交注释信息 容器ID:tag
# 可以理解为Git的commit或者虚拟机的快照
```

#### 删除

```shell
docker rm 容器ID

# 批量删除
docker rm $(docker ps -qa)
	# $() 是将里面命令的返回值作为参数传给外面的命令
	# docker ps -aq
		# -a 是显示所有容器(不论是否在运行)
		# -q 是静默显示，即只显示容器ID
```

### 示例

#### Nginx

> Docker部署运行**Nginx**

```bash
# 1. docker search nginx  搜索镜像
# 2. docker pull nginx    下载镜像
    i@ubuntu:/$ docker pull nginx
    
    Using default tag: latest
    latest: Pulling from library/nginx
    a076a628af6f: Pull complete 
    0732ab25fa22: Pull complete 
    d7f36f6fe38f: Pull complete 
    f72584a26f32: Pull complete 
    7125e4df9063: Pull complete 
    Digest: sha256:10b8cc432d56da8b61b070f4c7d2543a9ed17c2b23010b43af434fd40e2ca4aa
    Status: Downloaded newer image for nginx:latest
    docker.io/library/nginx:latest
# 3. docker run 运行测试

    # -d 后台运行
    # --name 自定义容器名称
    # -p 指定端口(宿主机端口:容器端口) 	访问宿主机3344端口会映射到容器内的80端口
    ### docker run -d --name nginx01 -p 3344:80 nginx

    i@ubuntu:/$ docker run -d --name nginx01 -p 3344:80 nginx
    
    360d290c713dc77fb93649bf33f3d7b14730cc41b0f6d5484985bd94206b6658
    i@ubuntu:/$ docker ps
    CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                  NAMES
    360d290c713d   nginx     "/docker-entrypoint.…"   4 seconds ago   Up 3 seconds   0.0.0.0:3344->80/tcp   nginx01
	
	## 测试nginx运行情况，访问宿主机3344端口，映射到容器的80端口
	i@ubuntu:/$ curl localhost:3344
	
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>

# 4. 外网访问
	浏览器输入 虚拟机Ip:3344即可进入Nginx欢迎页面
```

#### tomcat

> Docker 部署 **tomcat**

```shell
# 1. docker search tomcat  搜索镜像
# 2. docker pull tomcat    下载镜像
    i@ubuntu:/$ docker pull tomcat
    
    Using default tag: latest
    latest: Pulling from library/tomcat
    Digest: sha256:94cc18203335e400dbafcd0633f33c53663b1c1012a13bcad58cced9cd9d1305
    Status: Downloaded newer image for tomcat:latest
    docker.io/library/tomcat:latest
    
# 3. docker run 运行测试

    i@ubuntu:/$ docker run -d --name tomcat01 -p 3355:8080 tomcat
    
    924d5978de969899582f49c62d35de6886e84115fc62571d3f94e3eff6117023
    i@ubuntu:/$ docker ps
    CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                    NAMES
    924d5978de96   tomcat    "catalina.sh run"        17 seconds ago   Up 16 seconds   0.0.0.0:3355->8080/tcp   tomcat01
    360d290c713d   nginx     "/docker-entrypoint.…"   58 minutes ago   Up 58 minutes   0.0.0.0:3344->80/tcp     nginx01

	
	## 测试nginx运行情况，访问宿主机3344端口，映射到容器的80端口
    i@ubuntu:/$ curl localhost:3355
    
    <!doctype html><html lang="en"><head><title>HTTP Status 404 – Not Found</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 404 – Not Found</h1><hr class="line" /><p><b>Type</b> Status Report</p><p><b>Description</b> The origin server did not find a current representation for the target resource or is not willing to disclose that one exists.</p><hr class="line" /><h3>Apache Tomcat/9.0.41</h3></body></html>

	## 测试结果返回404
	## 是因为阿里云的镜像默认是最小镜像，需要把webapps.dist下的内容放到webapps下，重新访问成功
	
# 4. 外网访问
	浏览器输入 虚拟机Ip:3355即可进入tomcat欢迎页面
```

#### elasticsearch

> Docker 部署 **elasticsearch**

```shell
# 1. docker run 安装并运行
    i@ubuntu:/$ docker run -d --name elasticsearch01 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.6.2 
    
    Unable to find image 'elasticsearch:7.6.2' locally
    7.6.2: Pulling from library/elasticsearch
    ab5ef0e58194: Pull complete 
    c4d1ca5c8a25: Pull complete 
    941a3cc8e7b8: Pull complete 
    43ec483d9618: Pull complete 
    c486fd200684: Pull complete 
    1b960df074b2: Pull complete 
    1719d48d6823: Pull complete 
    Digest: sha256:1b09dbd93085a1e7bca34830e77d2981521a7210e11f11eda997add1c12711fa
    Status: Downloaded newer image for elasticsearch:7.6.2
    c83ecb6c53ca572eaf59f152ccf7d1743b9733a8ad428f12ff6094f783417c7d
    i@ubuntu:/$ docker ps
    CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                                            NAMES
    c83ecb6c53ca   elasticsearch:7.6.2   "/usr/local/bin/dock…"   27 seconds ago   Up 26 seconds   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   elasticsearch01

	## es暴露的端口较多
	## es运行十分占用内存
	
#2.  docker stats 查看内存占用情况
    i@ubuntu:/$ docker stats

    CONTAINER ID   NAME              CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O        PIDS
    c83ecb6c53ca   elasticsearch01   0.09%     1.244GiB / 7.221GiB   17.23%    3.64kB / 0B   2.23MB / 737kB   53

    CONTAINER ID   NAME              CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O        PIDS
    c83ecb6c53ca   elasticsearch01   0.09%     1.244GiB / 7.221GiB   17.23%    3.64kB / 0B   2.23MB / 737kB   53

    CONTAINER ID   NAME              CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O        PIDS
    c83ecb6c53ca   elasticsearch01   0.63%     1.244GiB / 7.221GiB   17.23%    3.64kB / 0B   2.23MB / 737kB   53

```

## Docker数据卷

### 概述

为了连接宿主机的文件和容器内的文件，实现容器的持久化。

容器与容器间也能实现文件共享。

```shell
# 1. 挂载目录 -v 主机目录:容器目录
	# 将主机的/home/docker/centos目录和容器内的/home目录双向关联
    i@ubuntu:~$ docker run -v /home/docker/centos:/home --name centos01 -it centos

    [root@966a70ddfc68 /]# i@ubuntu:~$ 
    i@ubuntu:~$ docker ps
    CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS          PORTS     NAMES
    966a70ddfc68   centos    "/bin/bash"   18 seconds ago   Up 17 seconds             centos01
```

```shell
   # 查看容器信息
   i@ubuntu:~$ docker inspect centos01
```

![image-20210202154340220](C:\Users\i\AppData\Roaming\Typora\typora-user-images\image-20210202154340220.png)

​		Source是宿主机目录，Destination是容器内地址

![image-20210202155113694](C:\Users\i\AppData\Roaming\Typora\typora-user-images\image-20210202155113694.png)

测试-->数据同步，容器内目录内容改变，宿主机内也改变。反之亦然。即实现了容器与宿主机文件的双向绑定。

### 实战：安装MySQL

```shell
# 官方安装启动命令 -e 配置环境，这里需要设置密码
$ docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag

# 1. 启动MySQL
	-p 端口映射
	-v 卷挂载
	-e 环境设置
	-d 后台启动
    i@ubuntu:/$ docker run -p 3310:3306 -v /home/docker/mysql/conf:/etc/mysql/conf.d -v /home/docker/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=1 --name mysql01 -d mysql:8.0

    e0508dc55a3b002145b1d7a32a93b84dc9dbdbdb448b77179f075fcc9c48b518

# 2. 在本机用navicat连接数据库测试是否连通-->成功

# 3. 删除容器测试宿主机目录内容是否还在
    i@ubuntu:/home/docker/mysql/data$ docker rm -f mysql01 
    mysql01
    i@ubuntu:/home/docker/mysql/data$ ls
     auto.cnf        ca.pem               ibdata1         mysql.ibd            sys
     binlog.000001   client-cert.pem      ib_logfile0     performance_schema   undo_001
     binlog.000002   client-key.pem       ib_logfile1     private_key.pem      undo_002
     binlog.000003  '#ib_16384_0.dblwr'   ibtmp1          public_key.pem
     binlog.index   '#ib_16384_1.dblwr'  '#innodb_temp'   server-cert.pem
     ca-key.pem      ib_buffer_pool       mysql           server-key.pem
```

发现容器删除后，挂载到本地的数据卷还存在，实现了容器数据的持久化！

### 匿名挂载与具名挂载

```shell
# 1. 匿名挂载，在-v时不指定主机目录，只指定容器目录
	# -v /etc/nginx
i@ubuntu:~$ docker run -d -v /etc/nginx --name nginx02 nginx
9163461b8c472e85cb16b1662d35f6d97853e5b7a94441795461cb8dc27b3efb

# docker volume 查看卷信息
    i@ubuntu:~$ docker volume ls
    DRIVER    VOLUME NAME
    local     fa318d942f443d4c18685cdf912e1b67d872b2eddd5ddf3952b94b79b0f0ecbf
	# 发现容器卷信息为16进制乱码

# 2. 具名挂载，在-v时不指定宿主机目录，但取别名来替代主机目录
	# -v 卷名:容器目录
	# -v named-nginx:/etc/nginx
    i@ubuntu:~$ docker run -d -v named-nginx:/etc/nginx --name nginx03 nginx
    a63817405a648af76e80d56d3e690245cba223af14fc9c9ee564356760d42872

    i@ubuntu:~$ docker volume ls
    DRIVER    VOLUME NAME
    local     named-nginx
    
# 通过docker volume inspect 卷名	来查看卷的具体信息
    i@ubuntu:~$ docker volume inspect named-nginx 
[
    {
        "CreatedAt": "2021-02-02T18:31:06+08:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/named-nginx/_data",  # 存放地址
        "Name": "named-nginx",
        "Options": null,
        "Scope": "local"
    }
]
```

所有Docker容器内的卷，没有指定，目录的情况下都是在宿主机`/var/lib/docker/volumes`目录下

大多数情况中我们使用的都是***具名挂载***。

```shell
# 查看宿主机中的卷目录
i@ubuntu:/var/lib/docker/volumes$ ls
5262e7fffc05ca7528ea1c22269aaf1c4a7c480ef9cfbf58f4e8f784129a7318  metadata.db
backingFsBlockDev                                                 named-nginx
fa318d942f443d4c18685cdf912e1b67d872b2eddd5ddf3952b94b79b0f0ecbf
```

***挂载总结：***

```shell
-v 容器内路径		  # 匿名挂载
-v 卷名:容器内路径      # 具名挂载
-v /宿主机路径:容器路径  # 指定路径挂载
```

***拓展：***

```shell
# -v 容器内路径:ro或rw  改变读写权限
	ro readonly # 只读
	rw readwrite# 读写
docker run -d -P --name nginx04 -v nginx3:/etc/nginx:ro nginx
docker run -d -P --name nginx04 -v nginx3:/etc/nginx:rw nginx
# 只要看到ro就说明这个路径只能通过宿主机来操作，容器内部是无法操作的！
```

### DockerFile挂载

```shell
# 创建编写dockerfile脚本
# dockerfile内容  命令(大写) 参数
FROM centos  # 以centos为基础镜像
  
VOLUME ["volume01","volume02"]  # 用于将生成的镜像自动创建两个目录匿名挂载到宿主机

CMD echo "-----end-----"

CMD /bin/bash
# 这里每个命令就是镜像中的一层
```

```shell
# 通过dockerfile打包生成镜像
# docker build [OPTIONS] PATH | URL | -
	# -f 指定通过哪个dockerfile
	# -t 生成镜像名称
	# . 为PATH路径，即为当前路径
i@ubuntu:~/docker-test-volume$ docker build -f dockerfile1 -t i/centos:0.1 .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM centos
 ---> 300e315adb2f
Step 2/4 : VOLUME ["volume01","volume02"]
 ---> Running in bbef076d89be
Removing intermediate container bbef076d89be
 ---> 61ade211504a
Step 3/4 : CMD echo "-----end-----"
 ---> Running in c56dd7e6c8e0
Removing intermediate container c56dd7e6c8e0
 ---> 72d1734ecb46
Step 4/4 : CMD /bin/bash
 ---> Running in a28419438715
Removing intermediate container a28419438715
 ---> 54288e8680c8
Successfully built 54288e8680c8
Successfully tagged i/centos:0.1

```

启动自己写的容器

![image-20210202194248259](C:\Users\i\AppData\Roaming\Typora\typora-user-images\image-20210202194248259.png)

这个目录就是我们生成镜像的时候自动挂载的。

![image-20210202194802330](C:\Users\i\AppData\Roaming\Typora\typora-user-images\image-20210202194802330.png)

### 数据卷容器

实现容器间数据共享

```shell
--volumes-from 容器ID   # 和指定容器一样的卷挂载

    i@ubuntu:~$ docker run -p 3310:3306 -v /home/docker/mysql/conf:/etc/mysql/conf.d -v /home/docker/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=1 --name mysql01 -d mysql:8.0
    c9092980b2f58f5fa76acd0375ba22510c074f624bbbc561cb3541ae7b479eda

    i@ubuntu:~$ docker run -p 3311:3306 --volumes-from mysql01 -e MYSQL_ROOT_PASSWORD=1 --name mysql02 -d mysql:8.0
    d8cac17a23eccc089ffa7b94259acaec253bb4618985467ec8095b44f9e18417

	i@ubuntu:~$ docker inspect mysql02
		...
        "Mounts": [
            {
                "Type": "bind",
                "Source": "/home/docker/mysql/conf",
                "Destination": "/etc/mysql/conf.d",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            },
            {
                "Type": "bind",
                "Source": "/home/docker/mysql/data",
                "Destination": "/var/lib/mysql",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            }
		...
	# 显然mysql01与mysql02卷挂载的位置相同，数据共享
```

## DockerFile

### 常用命令

```shell
FROM		# 基础镜像，一切从这里开始构建
MAINTAINER	# 镜像是谁写的，姓名+邮箱
RUN			# 镜像构建的时候需要运行的命令
ADD			# 如：tomcat镜像，就要添加tomcat压缩包！
WORKDIR		# 镜像的工作目录  如docker run xxx /bin/bash 	这个/bin/bash就是默认工作目录
VOLUME		# 挂载的目录(匿名挂载) -v
EXPOSE		# 保留端口配置 -p
ENV			# 镜像构建的时候设置环境变量！ -v
ONBUILD		# 当构建一个继承自该 DockerFile 的时候就会运行 ONBUILD 的指令。触发指令
COPY		# 类似ADD，将我们文件拷贝到镜像中

CMD			# 指定这个容器启动的时候要运行的命令，只有最后一个会生效，可被替代
ENTRYPOINT	# 指定这个容器启动的时候要运行的命令，可以追加命令
```

> CMD和ENTRYPOINT区别

```shell
# CMD命令是不追加的，追加命令的是直接覆写原命令

## dockerfile
FROM centos
CMD ["ls","-a"]

## build
i@ubuntu:~/myDockerFileDir$ docker build -f cmd-test -t cmd-test:0.1 .
Sending build context to Docker daemon  3.072kB
Step 1/3 : FROM centos
 ---> 300e315adb2f
Step 2/3 : MAINTAINER i<610253199@qq.com>
 ---> Running in f94ea5ad1cdf
Removing intermediate container f94ea5ad1cdf
 ---> c509dc7e705b
Step 3/3 : CMD ["ls","-a"]
 ---> Running in bb3b07bce52d
Removing intermediate container bb3b07bce52d
 ---> f851b2c378d2
Successfully built f851b2c378d2
Successfully tagged cmd-test:0.1

## run 
i@ubuntu:~/myDockerFileDir$ docker run -it cmd-test:0.1 
.   .dockerenv	dev  home  lib64       media  opt   root  sbin	sys  usr
..  bin		etc  lib   lost+found  mnt    proc  run   srv	tmp  var
	# 直接追加-l会因为没有-l命令而报错
i@ubuntu:~/myDockerFileDir$ docker run -it cmd-test:0.1 -l
docker: Error response from daemon: OCI runtime create failed: container_linux.go:370: starting container process caused: exec: "-l": executable file not found in $PATH: unknown.
	# 添加一个命令会直接运行该命令而不允许dockerfile中的命令，即覆盖了
	i@ubuntu:~/myDockerFileDir$ docker run -it cmd-test:0.1 ls -al
    total 56
    drwxr-xr-x   1 root root 4096 Feb  3 04:47 .
    drwxr-xr-x   1 root root 4096 Feb  3 04:47 ..
    -rwxr-xr-x   1 root root    0 Feb  3 04:47 .dockerenv
    lrwxrwxrwx   1 root root    7 Nov  3 15:22 bin -> usr/bin
    drwxr-xr-x   5 root root  360 Feb  3 04:47 dev
    drwxr-xr-x   1 root root 4096 Feb  3 04:47 etc
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 home
    lrwxrwxrwx   1 root root    7 Nov  3 15:22 lib -> usr/lib
    lrwxrwxrwx   1 root root    9 Nov  3 15:22 lib64 -> usr/lib64
    drwx------   2 root root 4096 Dec  4 17:37 lost+found
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 media
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 mnt
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 opt
    dr-xr-xr-x 413 root root    0 Feb  3 04:47 proc
    dr-xr-x---   2 root root 4096 Dec  4 17:37 root
    drwxr-xr-x  11 root root 4096 Dec  4 17:37 run
    lrwxrwxrwx   1 root root    8 Nov  3 15:22 sbin -> usr/sbin
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 srv
    dr-xr-xr-x  13 root root    0 Feb  3 04:47 sys
    drwxrwxrwt   7 root root 4096 Dec  4 17:37 tmp
    drwxr-xr-x  12 root root 4096 Dec  4 17:37 usr
    drwxr-xr-x  20 root root 4096 Dec  4 17:37 var


```

```shell
# ENTRYPOINT命令是追加的，增加的命令直接拼接在命令后

## dockerfile
FROM centos
ENTRYPOINT ["ls","-a"]

## build
i@ubuntu:~/myDockerFileDir$ docker build -f entrypoint-test -t entrypoint-test:0.1 .
Sending build context to Docker daemon  4.096kB
Step 1/2 : FROM centos
 ---> 300e315adb2f
Step 2/2 : ENTRYPOINT ["ls","-a"]
 ---> Running in c9d33a5f0b1b
Removing intermediate container c9d33a5f0b1b
 ---> f367bad8e69f
Successfully built f367bad8e69f
Successfully tagged entrypoint-test:0.1

## run
    i@ubuntu:~/myDockerFileDir$ docker run -it entrypoint-test:0.1 
    .   .dockerenv	dev  home  lib64       media  opt   root  sbin	sys  usr
    ..  bin		etc  lib   lost+found  mnt    proc  run   srv	tmp  var
	# 追加-l会直接拼接在ls -a后，成为ls -a -l
    i@ubuntu:~/myDockerFileDir$ docker run -it entrypoint-test:0.1 -l
    total 56
    drwxr-xr-x   1 root root 4096 Feb  3 04:55 .
    drwxr-xr-x   1 root root 4096 Feb  3 04:55 ..
    -rwxr-xr-x   1 root root    0 Feb  3 04:55 .dockerenv
    lrwxrwxrwx   1 root root    7 Nov  3 15:22 bin -> usr/bin
    drwxr-xr-x   5 root root  360 Feb  3 04:55 dev
    drwxr-xr-x   1 root root 4096 Feb  3 04:55 etc
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 home
    lrwxrwxrwx   1 root root    7 Nov  3 15:22 lib -> usr/lib
    lrwxrwxrwx   1 root root    9 Nov  3 15:22 lib64 -> usr/lib64
    drwx------   2 root root 4096 Dec  4 17:37 lost+found
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 media
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 mnt
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 opt
    dr-xr-xr-x 411 root root    0 Feb  3 04:55 proc
    dr-xr-x---   2 root root 4096 Dec  4 17:37 root
    drwxr-xr-x  11 root root 4096 Dec  4 17:37 run
    lrwxrwxrwx   1 root root    8 Nov  3 15:22 sbin -> usr/sbin
    drwxr-xr-x   2 root root 4096 Nov  3 15:22 srv
    dr-xr-xr-x  13 root root    0 Feb  3 04:55 sys
    drwxrwxrwt   7 root root 4096 Dec  4 17:37 tmp
    drwxr-xr-x  12 root root 4096 Dec  4 17:37 usr
    drwxr-xr-x  20 root root 4096 Dec  4 17:37 var
	# 直接写命令会因为无法拼接识别报错
	i@ubuntu:~/myDockerFileDir$ docker run -it entrypoint-test:0.1 ls -al
ls: cannot access 'ls': No such file or directory
```

### 实例

#### 构建自定义centos

编写DockerFile

```dockerfile
# DockerFile 内容
FROM centos
MAINTAINER i<610253199@qq.com>  # 作者信息

ENV MYPATH /usr/local  			# 环境变量
WORKDIR $MYPATH					# 工作目录设置为环境变量的值

RUN yum -y install vim			# 安装vim
RUN yum -y install net-tools	# 安装ifconfig等命令

EXPOSE 12345

CMD echo $MYPATH
CMD echo "----end----"
CMD /bin/bash
```

生成镜像

```shell
docker build -f dockerfile_cenos -t my_centos:0.1 .
# 查看镜像
i@ubuntu:~/myDockerFileDir$ docker images
REPOSITORY            TAG       IMAGE ID       CREATED              SIZE
my_centos             0.1       6c9e45e4e25e   About a minute ago   291MB
mysql                 8.0       c8562eaf9d81   2 weeks ago          546MB
tomcat                latest    040bdb29ab37   2 weeks ago          649MB
nginx                 latest    f6d0b4767a6c   3 weeks ago          133MB
centos                latest    300e315adb2f   8 weeks ago          209MB
portainer/portainer   latest    62771b0b9b09   6 months ago         79.1MB
elasticsearch         7.6.2     f29a1ee41030   10 months ago        791MB

```

运行测试

```shell
i@ubuntu:~/myDockerFileDir$ docker run -it my_centos:0.1 
[root@34369e08996c local]# pwd
/usr/local
[root@34369e08996c local]# vim
[root@34369e08996c local]# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
        RX packets 40  bytes 4396 (4.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# 测试发现vim,ifconfig等命令都可以使用
# pwd查看当前路径为/usr/local说明工作目录配置成功
```

#### 构建自定义Tomcat

1. 准备镜像文件 tomcat、jdk压缩包
2. 编写Dockerfile，建议命名`Dockerfile`，在build时会默认寻找文件名为Dockerfile的文件，这样可以不用`-f`指定文件。

```dockerfile
FROM centos
MAINTAINER i<610253199@qq.com>
# 添加文件
COPY README.txt /usr/local/README.txt
# 添加并自动解压镜像文件
ADD apache-tomcat-10.0.2.tar.gz /usr/local/
ADD jdk-8u181-linux-x64.tar.gz /usr/local/
# 安装vim
RUN yum -y install vim
# 添加默认工作目录
ENV MYPATH /usr/local
WORKDIR $MYPATH
# 添加JAVA环境变量
ENV JAVA_HOME /usr/local/jdk1.8.0_181
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
# 添加tomcat环境变量
ENV CATALINA_HOME /usr/local/apache-tomcat-10.0.2
ENV CATALINA_BASH /usr/local/apache-tomcat-10.0.2
# 把对应环境变量加到PATH中
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin

EXPOSE 8080
# 运行执行的命令
CMD /usr/local/apache-tomcat-10.0.2/bin/startup.sh && tail -F /usr/local/apache-tomcat-10.0.2/bin/logs/catalina.out
```

3. 生成镜像

```shell
# docker build
i@ubuntu:~/build_tomcat$ docker build -t mytomcat .
Sending build context to Docker daemon    197MB
Step 1/15 : FROM centos
 ---> 300e315adb2f
Step 2/15 : MAINTAINER i<610253199@qq.com>
 ---> Using cache
 ---> c509dc7e705b
Step 3/15 : COPY README.txt /usr/local/README.txt
 ---> Using cache
 ---> cde6702270df
Step 4/15 : ADD apache-tomcat-10.0.2.tar.gz /usr/local/
 ---> Using cache
 ---> 172b6cc45854
Step 5/15 : ADD jdk-8u181-linux-x64.tar.gz /usr/local/
 ---> Using cache
 ---> f50c75f4c05e
Step 6/15 : RUN yum -y install vim
 ---> Using cache
 ---> 6620af0f8b06
Step 7/15 : ENV MYPATH /usr/local
 ---> Using cache
 ---> 6fef2d36c0c1
Step 8/15 : WORKDIR $MYPATH
 ---> Using cache
 ---> 862d2c7f896e
Step 9/15 : ENV JAVA_HOME /usr/local/jdk1.8.0_181
 ---> Using cache
 ---> 9be03dd12479
Step 10/15 : ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
 ---> Using cache
 ---> 82d1beb9c267
Step 11/15 : ENV CATALINA_HOME /usr/local/apache-tomcat-10.0.2
 ---> Using cache
 ---> 35b05ccd9550
Step 12/15 : ENV CATALINA_BASH /usr/local/apache-tomcat-10.0.2
 ---> Using cache
 ---> d7e52e24b283
Step 13/15 : ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin
 ---> Using cache
 ---> 2862504ab66b
Step 14/15 : EXPOSE 8080
 ---> Using cache
 ---> c6e8d02b73ab
Step 15/15 : CMD /usr/local/apache-tomcat-10.0.2/bin/startup.sh && tail -F /usr/local/apache-tomcat-10.0.2/bin/logs/catalina.out
 ---> Using cache
 ---> 5274c14736a4
Successfully built 5274c14736a4
Successfully tagged mytomcat:latest
```

4. 运行测试

```shell
# docker run
i@ubuntu:~/build_tomcat$ docker run -d -p 9090:8080 -v tomcatWebappsTest:/usr/local/apache-tomcat-10.0.2/webapps/test -v tomcatLogs:/usr/local/apache-tomcat-10.0.2/logs mytomcat
e5ce670aacf1613fa54d65feb13ff6a6da0b7afdb0a1386eb4e9ab47e5fc7619
```

5. 访问测试

修改宿主机下绑定的tomcatWebappsTest卷目录，尝试访问。

```shell
# 创建jsp文件
i@ubuntu:/var/lib/docker/volumes/tomcatWebappsTest/_data$ cat index.jsp 
<html>
    <head>
        <title>Hello World</title>
    </head>
    <body>
        Hello World!<br/>
        <% 
        out.println("Your IP address is " + request.getRemoteAddr()); 
        %>
    </body>
</html>
```

外网访问http://192.168.169.137:9090/test/，成功返回页面

### 提交镜像

#### 阿里云仓库

![image-20210204130056934](C:\Users\i\AppData\Roaming\Typora\typora-user-images\image-20210204130056934.png)

```shell
# docker login
sudo docker login --username=rainnalv registry.cn-beijing.aliyuncs.com
#  docker tag 
# 为指定镜像打标签
i@ubuntu:/home$ sudo docker tag 5274c14736a4 registry.cn-beijing.aliyuncs.com/learning-repo/mydocker:0.1

i@ubuntu:/home$ docker images
REPOSITORY                                                TAG       IMAGE ID       CREATED         SIZE
mytomcat                                                  latest    5274c14736a4   3 hours ago     664MB
registry.cn-beijing.aliyuncs.com/learning-repo/mydocker   0.1       5274c14736a4   3 hours ago     664MB
entrypoint-test                                           0.1       f367bad8e69f   25 hours ago    209MB
cmd-test                                                  0.1       f851b2c378d2   25 hours ago    209MB
centos                                                    latest    300e315adb2f   8 weeks ago     209MB
hello-world                                               latest    bf756fb1ae65   13 months ago   13.3kB

# docker push
# 推送到镜像仓库
i@ubuntu:/home$ sudo docker push registry.cn-beijing.aliyuncs.com/learning-repo/mydocker:0.1 
The push refers to repository [registry.cn-beijing.aliyuncs.com/learning-repo/mydocker]
ea1f6c4c2a02: Pushed 
1316cbfb01f7: Pushed 
a16c51feab24: Pushed 
c8e60c7df6da: Pushed 
2653d992f4ef: Pushed 
0.1: digest: sha256:8d4d128873da08d37eacb8ace8444e45b139c1682e2c5e69dd484c891f560087 size: 1373
```

![image-20210204140400936](C:\Users\i\AppData\Roaming\Typora\typora-user-images\image-20210204140400936.png)

镜像提交成功！

#### DockerHub

```shell
# 登录
docker login
# 打tag
docker tag
# 提交
docker push
```

## Docker网络

…
