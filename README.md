# 流量超标自动关机脚本——超详细版

## 使用方法

### 1、简介

本脚本为腾讯云轻量服务器的流量监控脚本，可以定时监控多账户多地域多机器的流量使用情况，当已使用流量占总流量的百分比达到设定值（默认为95%）时会自动发出关机请求，避免流量超标，产生不必要的费用。

### 2、获取腾讯云API密钥

由于需要对腾讯云账号内的轻量服务器进行查询关机等操作，所以需要申请腾讯云API密钥。

先登录上腾讯云官网，然后点开下面这个链接：https://console.cloud.tencent.com/cam/capi

进入API密钥管理页面。

![](https://img.jpggod.com/file/jpggod/2021/04/13/c7722a3024b8aef6261497c189b402a2.png)

![](https://img.jpggod.com/file/jpggod/2021/04/13/9fa17baacdf6e973aa65ab94f185be9c.png)

保存SecretId、SecretKey

### 3、获取TG酱 token（用于通知关机信息）

TG酱依托于目前海外最流行之一的即时通讯软件Telegram（以下简称TG），如果你想启用改功能请申请一个账号 https://telegram.org/

然后在浏览器中点击 [@realtgchat_bot](https://t.me/realtgchat_bot)

或者在TG搜索

![](https://img.jpggod.com/file/jpggod/2021/04/13/bac97456a2769cbf505b8dc7a842b5da.png)

点击start后输入`/token` 机器人返回的值就是你的账号token

![](https://img.jpggod.com/file/jpggod/2021/04/13/c700a0744b48777ffcbe93d41ecb2f2b.png)

记下这个token

### 4、部署至GitHub Action

**4.1、fork项目**

由于需要使用自己的API密钥以及GitHub Action所以请务必先FORK本项目

![](https://img.jpggod.com/file/jpggod/2021/04/13/3193dd14526335de1a045751861849eb.png)

fork完之后接下来的操作请在自己账号下的刚fork的repository下进行操作

**4.2、添加密钥**

项目中按照 Setting--Secrets--New repository secert的顺序添加secrets

![](https://img.jpggod.com/file/jpggod/2021/03/30/7f88ec3aad0086502029348ebd3ee962.png)

依次添加之前保存的三个值

```
SecretId #腾讯云api密钥ID 以英文逗号分隔

SecretKey #腾讯云api密钥key 以英文逗号分隔

tgToken #TG酱token 加上引号""
```

多账户需要注意腾讯云账号密钥的ID 和KEY的顺序，不能乱，单账号直接复制粘贴即可，另外TG酱Token需要加上英文引号。添加后密钥显示名称会统一更换为大写字母。

![](https://img.jpggod.com/file/jpggod/2021/04/13/132c216968650da0a29cda75988e1f17.png)

依次添加完成即可。

### 效果检验

![](https://img.jpggod.com/file/jpggod/2021/04/13/96119564208093f62d3d64564885977a.png)

![](https://img.jpggod.com/file/jpggod/2021/04/13/6fd1cdb7d1c71a8063c560cfcc8252db.png)

点击build就可以看到输出日志了

![](https://img.jpggod.com/file/jpggod/2021/04/13/280fb13953d531e067222289e75f8fb2.png)

## 详细配置修改

流量百分比可以在LH.py中修改

![](https://img.jpggod.com/file/jpggod/2021/04/13/81056afbdf1cb6c3b9b4c1cb479bd37d.png)

如果自建TG消息机器人也可以在该文件中修改。

![](https://img.jpggod.com/file/jpggod/2021/04/13/bcbd0a2fa37ac48d9d7793f44bab78d1.png)

更改运行频率

默认每小时运行一次 想要修改频率可以修改 .github/workflows/LH.yml中schedule的cron参数，具体使用方法可以前往 [crontab使用方法](https://2demo.top/231.html)查看

![](https://img.jpggod.com/file/jpggod/2021/04/13/d4b5535109e4e1dba8d6a682363581b1.png)

AD:

腾讯云轻量购买地址：

288即可享受 1C1G30M香港高速CN2GIA服务器：https://curl.qcloud.com/ZYwQKs3G

热门活动还能折上折，详情联系QQ：3502399883

## 赞助：

![](https://www.vx.link/favicon.ico)

[微林](https://www.vx.link/)：提供数款效率工具，帮助您更专注于本质。