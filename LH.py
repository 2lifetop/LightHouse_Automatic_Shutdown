import json
import time
import requests
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models

gaojinData="流量告警"
gaojinResult="流量结果"
gaojinSatus="告警状态"

SecretId = os.environ["SecretId"]
SecretKey = os.environ["SecretKey"]

regions = ["ap-beijing", "ap-chengdu", "ap-guangzhou", "ap-hongkong", "ap-nanjing", "ap-shanghai", "ap-singapore", "ap-tokyo", "eu-moscow", "na-siliconvalley"]
percent = 0.80  # 流量限额，1表示使用到100%关机，默认设置为95%
tgToken = os.environ["tgToken"]

#钉钉机器人告警   
def sendmessage(message):
    #修改为你自己的钉钉webhook
    url = "https://oapi.dingtalk.com/robot/send?access_token=******************************************"
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8"
    }
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                "15*********"                                    #如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 1                                         #如果需要@所有人，这里写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)
    
#key参数  
def doCheck():
    try:
        # 参数
        ids = SecretId.split(",")
        keys = SecretKey.split(",")
        # print(ids)

        for i in range(len(ids)):
            for ap in regions:
                dofetch(ids[i], keys[i], ap)

    except TencentCloudSDKException as err:
        print(err)


def dofetch(id, key, region):
    # 以下不用管
    global gaojinSatus
    global gaojinResult
    cred = credential.Credential(id, key)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "lighthouse.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
    #获取实例列表
    req_instances = models.DescribeInstancesRequest()
    params = {}
    req_instances.from_json_string(json.dumps(params))
    resp_instances = client.DescribeInstances(req_instances) 
    s1=json.loads(resp_instances.to_json_string())['InstanceSet']
    for j in range (len(s1)):
        params.setdefault("InstanceIds",[]).append(s1[j]['InstanceId'])#获取实例ID        
    
    #获取实例流量
    req = models.DescribeInstancesTrafficPackagesRequest()
    req.from_json_string(json.dumps(params))  
    resp = client.DescribeInstancesTrafficPackages(req)
    s2=json.loads(resp.to_json_string())["InstanceTrafficPackageSet"]
    GB=1024*1024*1024
    for i in range (len(s2)):
        InstanceId= s2[i]['InstanceId']
        s3= s2[i]['TrafficPackageSet'][0]
        InstanceState =s1[i]["InstanceState"]
        TrafficPackageTotal = round(s3['TrafficPackageTotal']/GB,2)
        TrafficUsed = round(s3['TrafficUsed']/GB,2)
        TrafficPackageRemaining=str(round(s3['TrafficPackageRemaining']/GB,2)) 
        #告警数据
        global gaojinData
        gaojinData="流量告警数据:\n"+"已使用："+str(TrafficUsed)+"GB"+"\n"+"总流量："+str(TrafficPackageTotal)+"GB"+"\n"+"剩余量："+str(TrafficPackageRemaining)+"GB"
        #获取实例状态          
        print (i+1,"：",InstanceId,":","已使用：",TrafficUsed,"总流量：",TrafficPackageTotal,"剩余：",TrafficPackageRemaining)
        if (InstanceState == "RUNNING"):
            gaojinSatus="流量告警状态：运行中!"
            print("运行中")
            #实例流量超出限制自动关闭
            if (TrafficUsed/TrafficPackageTotal<percent):
                #告警结果：
                print("剩余流量充足")  
                gaojinResult="流量告警结果：剩余流量充足！"
            else:
                print(InstanceId,":","流量超出限制，自动关闭")
                req_Stop = models.StopInstancesRequest()
                params_Stop = {

                }
                params_Stop.setdefault("InstanceIds",[]).append(InstanceId)
                req_Stop.from_json_string(json.dumps(params_Stop))
                resp_Stop = client.StopInstances(req_Stop) 
                print(resp_Stop.to_json_string())
                #添加TG酱通知
                msgContent= InstanceId+ " ：流量超出限制，即将自动关机。" + "剩余流量：" + TrafficPackageRemaining+ "GB"
                msgUrl="https://tgbot-red.vercel.app/api?token="+ tgToken +"&message="+ msgContent
                #告警结果：
                gaojinResult="流量告警结果：流量超出限制，即将自动关机。\n"+"剩余流量：" + str(TrafficPackageRemaining)+ "GB"
                response= requests.get(url=msgUrl).text
                print (response)        
        else:
            if (TrafficUsed/TrafficPackageTotal<percent):
                #告警结果：
                print("剩余流量充足，将自动开机")
                req_Start = models.StopInstancesRequest()
                params_Start = {
                    "InstanceIds": [InstanceId]
                }
                req_Start.from_json_string(json.dumps(params_Start))
                resp_Start = client.StartInstances(req_Start)
                print(resp_Start.to_json_string())
                #添加TG酱通知
                msgContent= InstanceId+ " ：流量有剩余，即将自动开机。" + "剩余流量：" + TrafficPackageRemaining+ "GB"
                msgUrl="https://tgbot-red.vercel.app/api?token="+ tgToken +"&message="+ msgContent
                #告警结果：
                gaojinResult="流量告警结果：流量有剩余，即将自动开机。\n"+"剩余流量：" + str(TrafficPackageRemaining)+ "GB"
                response= requests.get(url=msgUrl).text
                print (response)
            else:
                gaojinSatus="流量告警状态：已关机!"
                print("流量告警状态：已关机!")
        
        #添加时间戳
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print ("--------------------")
#except TencentCloudSDKException as err: 
 #   print(err) 

if __name__ == '__main__':
     doCheck()
     gaojinTime="流量告警时间："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n"+"\n"
     gaojin=gaojinData+"\n"+"\n"+gaojinSatus+"\n"+"\n"+gaojinResult+"\n"+"\n"+gaojinTime
     #sendmessage(gaojin)
    # ck_kafka()
     pass
