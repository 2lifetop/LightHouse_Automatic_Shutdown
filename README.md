# LightHouse_Automatic_Shutdown
腾讯云轻量服务流量超出限制自动关机
## 使用方法
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

建议搭配crontab使用

如设置每个小时15分运行一次程序

```
crontab -e
15 * * * * /usr/bin/python3 /root/LightHouse_Automatic_Shutdown/LH.py >> /root/LightHouse_Automatic_Shutdown/LH.log 2>&1
```

## 输出

![](https://img.jpggod.com/file/jpggod/2021/03/13/4a104b8c8594f54b5a6273ed2249b088.png)

## 更多功能

- [ ] GitHub Actions版
- [ ] 腾讯云函数版
- [ ] server酱推送
- [ ] TG推送