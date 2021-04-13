# LightHouse_Automatic_Shutdown
腾讯云轻量服务流量超出限制自动关机
## 使用方法

[超详细版文档](./README_D.md)

## 2021年04月10日更新

人工合并多账户多地域检测代码

代码贡献者：[mosliu](https://github.com/mosliu/LightHouse_Automatic_Shutdown)

配置默认TG酱地址TG酱更改为自建版：[@realtgchat_bot](https://t.me/realtgchat_bot)

目前只需要配置

```
SecretId #腾讯云api密钥ID 以英文逗号分隔

SecretKey #腾讯云api密钥key 以英文逗号分隔

tgToken #TG酱token 加上引号""
```

SecretId、SecretKey需要 一 一对应

## 2021年03月30日更新

新增GitHub Action 实用性大大提升

只需要添加Secrets即可使用，添加方法

先fork本项目至自己的GitHub账号

项目 Setting--Secrets--New repository secert

![](https://img.jpggod.com/file/jpggod/2021/03/30/7f88ec3aad0086502029348ebd3ee962.png)



```
SecretId #腾讯云api密钥ID 

SecretKey #腾讯云api密钥key 

region #轻量服务器所在地域

tgBotUrl #TG酱url

tgToken #TG酱token
```

**获取地址**

SecretId、SecretKey ：https://console.cloud.tencent.com/cam/capi

region：[官方文档](https://cloud.tencent.com/document/product/1207/47564#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)

tgBotUrl：为tg酱网址，可以考虑[自建](https://github.com/anhao/TgMessage)或者使用现成的[TG酱](https://t.me/tg_jiang_bot) 
tg_token： 可以向TG酱发送`/mytoken` 获取

默认设置为流量达到95%自动关机，并向用户发出TG通知，可在LH.py文件中修改 percent 参数，数值0-1之间

默认每小时运行一次 想要修改频率可以修改 .github/workflows/LH.yml中schedule的cron参数，具体使用方法可以前往 [crontab使用方法](https://2demo.top/231.html)查看



# 服务器运行

### 安装腾讯云Python SDK 3.0
```
pip3 install tencentcloud-sdk-python #python3
```
### 参数

```
    SecretId=""
    SecretKey=""
    region=""
    percent= 0.95
    tgBotUrl="https://dianbao.vercel.app/send/"
    tgToken=""

```

SecretId,SecretKey 请前往腾讯云访问管理控制台获取：https://console.cloud.tencent.com/cam/capi

![](https://img.jpggod.com/file/jpggod/2021/03/13/0b27e56b61dc83fcb881dc39a2747e8d.png)

region 为服务器所在地域具体参照下表

| 华北地区(北京)       | ap-beijing       |
| -------------------- | ---------------- |
| 西南地区(成都)       | ap-chengdu       |
| 华南地区(广州)       | ap-guangzhou     |
| 港澳台地区(中国香港) | ap-hongkong      |
| 华东地区(南京)       | ap-nanjing       |
| 华东地区(上海)       | ap-shanghai      |
| 亚太东南(新加坡)     | ap-singapore     |
| 亚太东北(东京)       | ap-tokyo         |
| 欧洲地区(莫斯科)     | eu-moscow        |
| 美国西部(硅谷)       | na-siliconvalley |

[官方文档](https://cloud.tencent.com/document/product/1207/47564#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)

percent为 套餐内已使用流量占比 默认设置为 0.95，超出后自动关机
tgBotUrl 为tg酱网址，可以考虑[自建](https://github.com/anhao/TgMessage)或者使用现成的[TG酱](https://t.me/tg_jiang_bot)  默认使用TG酱网址
tg_token 可以向TG酱发送`/mytoken` 获取
![](https://img.jpggod.com/file/jpggod/2021/03/29/7d488dce8aec13086276be37ff0a9e84.png)

建议搭配crontab使用

如设置每个小时15分运行一次程序

```
crontab -e
15 * * * * /usr/bin/python3 /root/LightHouse_Automatic_Shutdown/LH.py >> /root/LightHouse_Automatic_Shutdown/LH.log 2>&1
```

## 输出

![](https://img.jpggod.com/file/jpggod/2021/03/29/cd072a6393deac77d09acb6695ea58af.png)
TG酱
![](https://img.jpggod.com/file/jpggod/2021/03/29/5bc2de7b70e91cf7e1bda802c91ff325.png)

## 更多功能

- [x] GitHub Actions版
- [ ] 腾讯云函数版
- [ ] server酱推送
- [x] TG推送

博客地址：https://2demo.top/222.html
