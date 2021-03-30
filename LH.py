import json
import time
import requests
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models
try:
    #参数
    SecretId = os.environ["SecretId"]
    SecretKey = os.environ["SecretKey"]
    region= os.environ["region"]
    percent= 0.95 #流量限额，1表示使用到100%关机，默认设置为95%
    tgBotUrl= os.environ["tgBotUrl"]
    tgToken= os.environ["tgToken"]

    # 以下不用管
    cred = credential.Credential(SecretId,SecretKey)
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
        #获取实例状态          
        print (i+1,"：",InstanceId,":","已使用：",TrafficUsed,"总流量：",TrafficPackageTotal,"剩余：",TrafficPackageRemaining)
        if (InstanceState == "RUNNING"):
            print("运行中")
            #实例流量超出限制自动关闭
            if (TrafficUsed/TrafficPackageTotal<percent):
                print("剩余流量充足")
                          
                
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
                msgUrl= tgBotUrl + tgToken +"/"+ msgContent
                response= requests.get(url=msgUrl).text
                print (response)        
        else:
            print("已关机")
        
        #添加时间戳
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print ("--------------------")
except TencentCloudSDKException as err: 
    print(err) 
