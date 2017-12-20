#-*- coding: utf-8 -*-
import os
import cv2.cv as cv
from facepp import API, File
API_KEY = "WqoaSriNwvTQOguKuZc-6HzC_2DpEH_H"
API_SECRET = "tKpDo2A7W8RQv2UqBiNnJzAQ1V0bnccO"
api = API(API_KEY, API_SECRET)
from pprint import pformat
def encode(obj):
    if type(obj) is unicode:
        return obj.encode('utf-8')
    if type(obj) is dict:
        return {encode(v): encode(k) for (v, k) in obj.iteritems()}
    if type(obj) is list:
        return [encode(i) for i in obj]
    return obj
def print_result(hit, result):
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))

def GetPicFile(path, list_file):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            pass
        elif os.path.splitext(file_path)[1] == '.JPG':
            list_file.append(file_path)
def GetFilename(file):
    return os.path.splitext(file)[0].split('/')[-1]
def AddPicToSet():
    filename = raw_input("Enter setid file path: ")
    path = raw_input("Enter Picture path: ")
    if os.path.exists(filename):
        input=open(filename)
        setid=input.readlines()[0].strip('\n')
        list_file=[]
        GetPicFile(path,list_file)
        Face = {}
        print(list_file)
        for i in list_file:
            res = api.detect(image_file=File(i))
            while (res.has_key("error_message") != 0):
                res = api.detect(image_file=File(i))
            Face[GetFilename(i)] = res["faces"][0]["face_token"]
        for k,v in Face.items():
            result = api.face.setuserid(face_token=v, user_id=k)
            while (result.has_key("error_message")!=0):
                result = api.face.setuserid(face_token=v, user_id=k)
            print_result("set id",result)
            result1 = api.faceset.addface(outer_id=setid, face_tokens=v)
            while(result1.has_key("error_message")!=0):
                result1 = api.faceset.addface(outer_id=setid, face_tokens=v)
            print_result("add face", result1)
def GenerateSet(path):
    filename = os.path.join(path,'setid.txt')
    if not os.path.isdir(path):
        os.makedirs(path)
    if os.path.exists(filename):
        input=open(filename)
        setid=input.readlines()[0].strip('\n')
        input.close()
        return setid
    else:
        output = open(filename, 'w')
        ret = api.faceset.create(outer_id=path.split('/')[-1])
        while (ret.has_key("error_message") != 0):
            ret = api.faceset.create(outer_id=path.split('/')[-1])
        print_result("faceset create", ret)
        setid=ret["outer_id"]
        output.write(setid)
        output.close()
        list_file=[]
        GetPicFile(path,list_file)
        Face = {}
        print(list_file)
        for i in list_file:
            res = api.detect(image_file=File(i))
            while (res.has_key("error_message") != 0):
                res = api.detect(image_file=File(i))
            Face[GetFilename(i)] = res["faces"][0]["face_token"]
        for k,v in Face.items():
            result = api.face.setuserid(face_token=v, user_id=k)
            while (result.has_key("error_message")!=0):
                result = api.face.setuserid(face_token=v, user_id=k)
            print_result("set id",result)
            result1 = api.faceset.addface(outer_id=setid, face_tokens=v)
            while(result1.has_key("error_message")!=0):
                result1 = api.faceset.addface(outer_id=setid, face_tokens=v)
            print_result("add face", result1)
        return setid
def register(filepath,setid,list):
    ret = api.detect(image_file=File(filepath))
    while (ret.has_key("error_message") != 0):
        ret = api.detect(image_file=File(filepath))
    #print_result("detect", ret)
    if not len(ret['faces']):
        print("相片中没有人脸")
        return
    search_result = api.search(face_token=ret["faces"][0]["face_token"], outer_id=setid)
    while (search_result.has_key("error_message") != 0):
        search_result = api.search(face_token=ret["faces"][0]["face_token"], outer_id=setid)
    if(search_result["results"][0]["confidence"]>=search_result["thresholds"]["1e-5"]):
        print(search_result['results'][0]['user_id'])
        list.append(search_result['results'][0]['user_id'])
    else:
        print("不在名单中")
signed=[]
path = raw_input("Enter Picture path: ")
setid=GenerateSet(path)
capture = cv.CaptureFromCAM(0)
while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("camera",img)
    key = cv.WaitKey(10)
    if key == 27:
        break
    if key == ord(' '):
        filepath = os.path.join(path,"face.jpg")
        cv.SaveImage(filepath,img)
        register(filepath,setid,signed);

del(capture)
cv.DestroyWindow("camera")
signed=list(set(signed))
with open('signed.txt', 'w') as f:
    for i in signed:
        f.writelines(encode(i))
