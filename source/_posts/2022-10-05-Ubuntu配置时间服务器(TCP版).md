---
title: Ubuntu配置时间服务器(TCP版)
date: 2022-10-05 22:18:54 +0800
categories: [配置]
tags: [环境部署, Ubuntu, linux]
---

## 问题提出

最近由于二十大要召开，用的物联网卡又只能走TCP访问指定IP的服务器，为了同步时间，需要在服务器搭建一个时间服务器，主流都是使用udp的ntp协议，但是由于不可抗力，无法使用udp，遂只能使用支持TIME协议的服务器，一通搜索终于找到支持rdate的服务器搭建方式：**xinetd**。这个东西其实不是用来搭建时间服务器的，貌似是个后台服务管理的程序。

![image-20220929115746809](http://qiniu.rainna.xyz/image-20220929115746809.png)

## 具体操作

### 安装xinetd

```shell
sudo apt update
sudo apt install xinetd
```

### 修改配置文件

`xinetd`的配置文件位置在`/etc/xinetd.d`下

Ubuntu下的配置文件如图：

![image-20220929120546359](http://qiniu.rainna.xyz/image-20220929120546359.png)

```shell
sudo vim /etc/xinetd.d/time
```

内容如图：

![image-20220929120853257](http://qiniu.rainna.xyz/image-20220929120853257.png)

修改第一个`disable  = yes`为`disable = no`即可，第二个是udp协议，不需要修改，修改完毕如图。

![image-20220929120812549](http://qiniu.rainna.xyz/image-20220929120812549.png)

### 启动xinetd服务

```shell
sudo service xinetd restart
```

### 查看是否启动成功

```shell
sudo service xinetd status
```

![image-20220929121106859](http://qiniu.rainna.xyz/image-20220929121106859.png)

若`start working`是**<u>1</u>** available service，则表示启动成功。

### 验证

使用`rdate`查看能否正常访问时间服务。

1. 安装`rdate`： `sudo apt install rdate`

2. 访问时间服务器： `sudo rdate -p localhost`

   - 这里是在服务器本地测试是否成功，如果没问题会输出如下结果

     ![image-20220929121454909](http://qiniu.rainna.xyz/image-20220929121454909.png)

3. 外网测试：`sudo rdate -p {IP}` 这里的IP是服务器的IP，如果显示连接拒绝，多半是防火墙或者安全组**37**端口没放开，前往对应的云服务提供商控制台开放37端口 TCP访问权限即可，另外也需要本地防火墙允许通过。