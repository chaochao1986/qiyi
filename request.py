# -*- coding:utf-8 -*-
#!/bin/python env
import json
import string
import urllib2

from JsonValue import getByMultiLevelKey

from jsonSplit import splitJson
from protobuf_to_dict import dict_to_protobuf
from  show import bid_request_extensions_pb2
from  show import bid_request_pb2


class ProRequest():
    def __init__(self):
        self.url=""
        self.bidRequest={}
        self.response={}
    def findJson(self,findName,tempString):
        if string.find(tempString, findName) != -1:
            temp = splitJson(str(findName), tempString)
            rootJson = json.loads(json.dumps(temp))
            tempRequest = ''.join(rootJson)
            rootTemp = json.loads(tempRequest)
            return rootTemp
        else:
            return ""

    def getRequest(self,url,findName):
        resonse=urllib2.urlopen(url)
        resonseTemp=resonse.read()
        rootTemp=self.findJson(findName,resonseTemp)
        if rootTemp!="":
            self.bidRequest=rootTemp[findName]
        else:
             return ""



    def showRequestProto(self):
        showBidRequest=bid_request_pb2.BidRequest()

        showBidRequest.id=self.bidRequest["id"]
        dict_to_protobuf(self.bidRequest["user"],showBidRequest.user)
        dict_to_protobuf(self.bidRequest["root_request"],showBidRequest.Extensions[bid_request_extensions_pb2.root_request])
        dict_to_protobuf(self.bidRequest["site"],showBidRequest.site)
        dict_to_protobuf(self.bidRequest["device"],showBidRequest.device)
        for i in self.bidRequest["imp"]:
            dict_to_protobuf(i,showBidRequest.imp.add())

        dict_to_protobuf(self.bidRequest["user_model"],showBidRequest.Extensions[bid_request_extensions_pb2.user_model])
        showBidRequest.Extensions[bid_request_extensions_pb2.sdk_version]=self.bidRequest["sdk_version"]
        dict_to_protobuf(self.bidRequest["dmp_audience"],showBidRequest.Extensions[bid_request_extensions_pb2.dmp_audience])
        dict_to_protobuf(self.bidRequest["user_tag"],showBidRequest.Extensions[bid_request_extensions_pb2.user_tag])
        showBidRequest.Extensions[bid_request_extensions_pb2.mobile_model_key]=self.bidRequest["mobile_model_key"]
        showBidRequest.Extensions[bid_request_extensions_pb2.should_request_show]=self.bidRequest["should_request_show"]



        data=showBidRequest.SerializeToString()

        header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
        url="http://10.10.132.213:7103/show2?"

        req=urllib2.Request(url=url,data=data,headers=header_dict)

        response=urllib2.urlopen(req)
        self.response=response.read()
        return response.read()

    def Response(self,responseTemp):
        if string.find(self.response,responseTemp):
            temp=self.response.rindex('}')
            responseResult=splitJson(responseTemp,self.response[:temp])
            return responseResult+"}"
        else:
            return False



    def compareResponse(self,inputResult,keyList,keyworld):
        inputTemp=json.loads(inputResult)
        standWorld=getByMultiLevelKey(inputTemp,keyList,None)
        if standWorld==None:
            return False
        elif standWorld==keyworld:
            return True
        else:
            return False




proTemp=ProRequest()
#proTemp.getRequest("http://10.10.132.213/show2?i=862636033621234&s=bb34dc0c3853487d8f60cfeffe9f57ec&u=862636033621234&e=EAo7DAgHCANVbgQFBgcNDhcHOhdSDQEBAW8EAwQJCQ9BU28XU1ENAgFvF1NUDQAAQUU8Rw0JHgMfbxdVUQ0JEBYXYgAWWV1VWGIJUgcFCQVAVD5UCQAECAc8VwkIUVtXElc6UwBTB1UGZxdZXUMFBkFTbwEAAAAAAW5yAAAACBAdXnldWA0AFl0vDAAWXEwLRFBrCAIBAgABeV1GDQEBEBxeEGFgfxtiCDIXXVFTBVVBWWZXCgAFCgQ7CwcICl1QVw1iARZeRw0BeV4NAhZXRUxRbwEWX0NGDGofARZAVwtBRS9CDQAWQQw8RQoBABRFGFluHUNECgMBeUJDDQEeRQdeah8CCR4AAWsXRA0GAQ5FUWkFAgQIA1A7VQBRBgsDQVBsAQZUBgNXbwUEAxZOC0FFKVRZVA1UBG9UCVIIXlJIWj1QAFEFUlJqBAIBAQxQEFU7BVJSARZGYgEWSQ0J&h=1522661268893&a=qc_100001_100086&at=10,11&g=10.3.4.134&dl=100","BidRequest")
try:
    proTemp.getRequest("http://10.10.132.213/show2?i=354765085351773&s=d945021b2bf0fffec7adb7a07ec2a5c1&u=354765085351773&e=EAo7DAkABQgBaAhSBlULABBWOQAWUg0BAG8BAwcCDQBFW28BFlNRDQVuBRZTVAUHSFpmF1NGDQkfaR8AFlReRkxSagIEAFVVB2YJBlUCCQJIW2cIVAIICAE8UgQIUV1TRlBoVAQBCFFTOggAUQgBU0AHalJRBQgFAj0DAwkGWQJDBzkXVVENARc4RQ0BFlFbFApiAgABCAMJbVJRCQBbVxAAZglWBwQBV2wAAVUCWgNHVG4XWV1DDQQdAXVzcQ9wQVBvAQAAAAAXMwwWXFgFBlcPLwwAFlxEDGwGAgIJDgVBU3ldRg0EABcyDGN9HX8PRFNvF11RUw0BbQsAAAoIBktTbwsAAAoAAXlfDQAWVkFMUnleDQIWX0JiAwAAFldFB15oHwAWQF1HYgUeAB4KGERXZwYWQF8NAHlBQw0AHkdMACsLARZDQwxuF0NGDQ0YQlBxAQADFkQMbgEABAQKBkMAbwJRBAcIATkFBgBUCw5CAD0HUgRVVQJ5Rw0AFk5TGAdiVwYCCVMEPlAJUgBZBxQAalcJBwhSBToJUlQBWwBIUWgXRw0AFkhiAQ%3D%3D&h=1527664648523&a=qc_100001_100086&at=1&g=10.3.4.132&dl=100","BidRequest")
except Exception:
    proTemp.getRequest("http://10.10.132.213/show2?i=354765085351773&s=d945021b2bf0fffec7adb7a07ec2a5c1&u=354765085351773&e=EAo7DAkABQgBaAhSBlULABBWOQAWUg0BAG8BAwcCDQBFW28BFlNRDQVuBRZTVAUHSFpmF1NGDQkfaR8AFlReRkxSagIEAFVVB2YJBlUCCQJIW2cIVAIICAE8UgQIUV1TRlBoVAQBCFFTOggAUQgBU0AHalJRBQgFAj0DAwkGWQJDBzkXVVENARc4RQ0BFlFbFApiAgABCAMJbVJRCQBbVxAAZglWBwQBV2wAAVUCWgNHVG4XWV1DDQQdAXVzcQ9wQVBvAQAAAAAXMwwWXFgFBlcPLwwAFlxEDGwGAgIJDgVBU3ldRg0EABcyDGN9HX8PRFNvF11RUw0BbQsAAAoIBktTbwsAAAoAAXlfDQAWVkFMUnleDQIWX0JiAwAAFldFB15oHwAWQF1HYgUeAB4KGERXZwYWQF8NAHlBQw0AHkdMACsLARZDQwxuF0NGDQ0YQlBxAQADFkQMbgEABAQKBkMAbwJRBAcIATkFBgBUCw5CAD0HUgRVVQJ5Rw0AFk5TGAdiVwYCCVMEPlAJUgBZBxQAalcJBwhSBToJUlQBWwBIUWgXRw0AFkhiAQ%3D%3D&h=1527664648523&a=qc_100001_100086&at=1&g=10.3.4.132&dl=100","BidRequest")

proTemp.showRequestProto()
temp=proTemp.Response("leafResponse0")
listTemp=["leafResponse0","getSpecialAds","frequencySignalHandler",0,"deletedOrderItem",0,"orderItemDetail","order_item_id"]
print proTemp.compareResponse(temp,listTemp, 9111111114621)