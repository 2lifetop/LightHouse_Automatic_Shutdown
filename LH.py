import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models
try:
    #参数
    SecretId=""
    SecretKey=""
    region=""
    percent= 0.95

    # 以下不用管
    cred = credential.Credential(SecretId,SecretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "lighthouse.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
    #获取实例列表
    req_instances = models.DescribeInstancesRequest()
    params = {

    }
    req_instances.from_json_string(json.dumps(params))
    resp_instances = client.DescribeInstances(req_instances) 
    s1=json.loads(resp_instances.to_json_string())['InstanceSet']
    for j in range (len(s1)):
        params.setdefault("InstanceIds",[]).append(s1[j]['InstanceId'])

    #获取实例流量
    req = models.DescribeInstancesTrafficPackagesRequest()
    req.from_json_string(json.dumps(params))  
    resp = client.DescribeInstancesTrafficPackages(req)
    s2=json.loads(resp.to_json_string())["InstanceTrafficPackageSet"]
    GB=1024*1024*1024
    for i in range (len(s2)):
        InstanceId= s2[i]['InstanceId']
        s3= s2[i]['TrafficPackageSet'][0]          
        print (i+1,"：",InstanceId,":","已使用：",round(s3['TrafficUsed']/GB,2),"总流量：",round(s3['TrafficPackageTotal']/GB,2),"剩余：",round(s3['TrafficPackageRemaining']/GB,2))
        #实例流量超出限制自动关闭

        if (round(s3['TrafficUsed']/GB,2)/round(s3['TrafficPackageTotal']/GB,2)<percent):
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
except TencentCloudSDKException as err: 
    print(err) 
