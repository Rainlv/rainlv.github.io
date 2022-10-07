---
title: Ubuntu下Selenium自动上传
date: 2022-10-05 22:19:09 +0800
categories: [踩坑]
tags: [python, linux, Selenium, Ubuntu]
---

## 问题描述

最近参与了一个小比赛，成果提交方式是提交Docker镜像，镜像执行在服务端进行，执行完毕会返回执行结果

比赛存在使用随机seed控制场景，导致结果会有好坏变化的情况。为了得到一个较好的成绩，可以通过不断提交镜像来刷分。

但是我总是忘记上传，于是想到抓包使用爬虫加定时任务的方式取代人工上传。

但是直接抓包，并没有找到文件的上传接口，因为有断点续传的功能，估计没有直接的上传接口（大概）。

想到使用Selenium来模拟点击实现自动上传。

但是，上传按钮不是传统的`input`标签，是一个`button`，不能通过直接`send_key`来指定文件，只能通过模拟选择文件上传。

## 解决方案

点击button会弹出OS级别的弹框，并将窗口焦点聚焦于弹框中，因此只需要模拟输入文件路径，并点击`打开`按钮，即可完成选择文件上传的功能。

![image-20220925202318296](http://qiniu.rainna.xyz/image-20220925202318296.png)

> Ubuntu中，在文件管理器中输入`ctrl`+`l`出现路径输入框，输入完毕，输入`enter`或者`alt`+`o`表示打开文件，相当于点击右上角的`打开(O)`
>
> ![image-20220926165308535](http://qiniu.rainna.xyz/image-20220926165308535.png)

对于Windows系统，可以使用`pywin32`或者`SendKeys等库完成上述流程，但是对于Linux系统似乎没有看到类似的博客，遂一通搜索找到了一个`pyqutogui`的跨平台的自动化库，可以程序控制键鼠的输入。具体API参考[官方文档](https://github.com/asweigart/pyautogui)。

## 具体实现

不多说，直接上代码

```python
def Ubuntu_autogui_uploader(self, filk_path):
    import pyautogui
    pyautogui.hotkey('alt', 'o')
    pyautogui.typewrite(filk_path)
    # 防止中文输入法
    pyautogui.press("enter")
    pyautogui.hotkey('alt', 'o')
```

- 这里又输入了`enter`又使用了`alt`+`o`是为了防止输入法为中文时，输入字符没有正确进入输入框，追加一个`enter`确保进入，若能保证为英文输入法，可以删去这一行。

迁移到Windows也很简单，Windows相比Ubuntu少了一步`Ctrl`+`L`，默认焦点就在输入框上：

```python
def win_autogui_uploader(self):
    import pyautogui
    pyautogui.typewrite(self.image_tar_path)
    # 防止中文输入法
    pyautogui.press("enter")
    pyautogui.hotkey('alt', 'o')
```

## 总结

虽然可以实现自动上传，但是基于GUI实现的上传，需要保证出现上传弹窗时焦点是在弹窗上，也就是鼠标不能点击其他区域，或出现其他高等级的弹窗导致窗口失焦，否则会导致文本无法输入，而导致自动化流程中断。

