---
title: Geoserver安装配置GDAL扩展
date: 2022-06-29 09:12:46 +0800

---

## 问题描述

按照[官网](https://docs.geoserver.org/stable/en/user/data/raster/gdal.html#installing-gdal-extension)和一些[博客](https://blog.csdn.net/ys_ys_y/article/details/106499154)的操作流程安装GDAL扩展后，发现创建数据存储时没有出现img等格式

查看geoserver控制台，发现加载GDAL的dll文件时出错

![image-20220629085619718](http://qiniu.rainna.xyz/202206290856915.png)

> 截图是在总结问题时截的，配置完成后似乎不能复现原来的bug，日志略有不同



## 原因分析

当时下载的预编译GDAL库来自[gisinternals](https://www.gisinternals.com/release.php)，可以看到其`{GDAL_HOME}/bin/gdal/java`下的dll并不是gdaljni.dll

![image-20220629091008309](http://qiniu.rainna.xyz/202206290910407.png)

而是`gdalalljni.dll`，重命名成`gdaljni.dll`，并复制一份相同的并命名为`gdalconstjni.dll`

> gdal库含有gdal和gdalconst两个模块，猜测gdalall是将两个模块放在一起了，但是geoserver可能是按文件名加载的，所有会出现上述问题。