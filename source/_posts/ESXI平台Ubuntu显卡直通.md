---
title: ESXI平台Ubuntu显卡直通
date: 2023-04-30 17:41:09
categories: 环境配置
tags: [nvidia]
---



### 问题1

实验室新装了几台服务器，加入vSphere集群，配置显卡直通后，创建的windows虚拟机可以正常安装Nvidia驱动，`nvidia-smi`命令可以显示显卡信息，但是创建的ubuntu虚拟机`nvidia-smi`一直无法显示显卡信息，返回`no devices were found`。



`sudo lspci |grep -i VGA`

```
03:00.0 VGA compatible controller: NVIDIA Corporation Device xxxxx
```

`dmesg`

```
[ 1606.332778] NVRM: GPU 0000:03:00.0: RmInitAdapter failed! (0x26:0x56:1463)
[ 1606.332912] NVRM: GPU 0000:03:00.0: rm_init_adapter failed, device minor number 0
[ 1607.004207] NVRM: GPU 0000:03:00.0: RmInitAdapter failed! (0x26:0x56:1463)
[ 1607.004349] NVRM: GPU 0000:03:00.0: rm_init_adapter failed, device minor number 0
```



### 环境

- 平台 ESXI 6.7 Update3
- 虚拟机系统 Ubuntu18.04（16.x也试过同样问题）
- 显卡：3090 * 8



### 解决方案

NVDIA论坛有类似问题，中文社区貌似没有搬运过类似的方法，大多是设置高级参数，打补丁之类的方法。[传送门](https://forums.developer.nvidia.com/t/nvidia-smi-no-devices-were-found-vmware-esxi-ubuntu-server-20-04-03-with-rtx3070/202904/25)



1. 禁用nouveau

```
touch /etc/modprobe.d/blacklist-nvidia-nouveau.conf

cat /etc/modprobe.d/blacklist-nvidia-nouveau.conf << EOF
blacklist nouveau
options nouveau modeset=0
EOF
```

2. NVDIA内核参数

```
touch /etc/modprobe.d/nvidia.conf

cat >> /etc/modprobe.d/nvidia.conf << EOF
options nvidia NVreg_OpenRmEnableUnsupportedGpus=1
EOF
```

3. 应用更改

```
sudo update-initramfs -u
```

4. 重启

5. 下载驱动（官网）
6. 安装驱动

```
sudo .\nvidia-derive-filename.run -m=kernel-open
```

7. 重启

 

## 问题2

vsphere中的虚拟机配置直通GPU后，启动时出现模块“DevicePowerOn”打开电源失败。



### 环境

- 平台 ESXI 6.7
- 显卡 Tesla K80



### 解决方案

设置高级参数

```
pciPassthru.use64bitMMIO=TRUE
pciPassthru.64bitMMIOSizeGB=64
```

具体操作如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/8a287079595f4eb1befca3dec47e2d6b.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/9cf4da550288431d8ac1caaf69642c93.png)