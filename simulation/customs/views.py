import json
from datetime import datetime
import time

from django.core.serializers import serialize
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
# Create your views here.
from .main import *
import random
import simpy
from .models import tuple

#模擬的參數
RANDOM_SEED=0
NUM_POLICE=1#關務總數
TIME_CONSUMING=5500 #處理時間
CLIENT_INTERVAL=5500 #顧客間隔
arrivalCV=200
serviceTimeCV=200
resultList=[]
SimBoolean=True
resetBool=False
intervalList=[]
serviceList=[]
arrivalList=[]
numfortest=3000
customerNum=0
adjustmentTime=0

def sim(request):
    resultList.clear()
    record = tuple.objects.all()
    return render(request, 'sims.html', {
        'current_time': str(datetime.now()),
        'temp':str(TIME_CONSUMING),
        'record':record
    })


#模擬本體

class Customs(object):
    #海關
    def __init__(self,env,num_police,time_consuming):
        self.env=env
        self.police=simpy.Resource(env,num_police)
        self.time_consuming=time_consuming
        self.allClient=0
        self.accomplishClient=0

    def processing(self,client,i):
        if TIME_CONSUMING==0:
            print("police go eat lunch")
        else:
            resultList.append(env.now - arrivalList[i]-adjustmentTime)
            tmp=abs(random.normalvariate(TIME_CONSUMING,serviceTimeCV))
            serviceList.append(tmp)
            yield self.env.timeout(tmp)
            self.accomplishClient += 1
            #print("目前服務用戶數:%d , 已完成用戶數:%.2f" % (self.allClient, self.accomplishClient))

def Client(env,name,customs,i):
    arrivalList.append(env.now-adjustmentTime)
    #print("%s 到達海關 at %.2f" %(name,env.now))
    with customs.police.request() as request:
        yield request
        #print('%s 接受檢查   at %.2f.' % (name, env.now))
        yield env.process(customs.processing(name,i))
        #print('%s 離開海關 at %.2f.' % (name, env.now))

def setup(env,num_police,time_consuming,CLIENT_INTERVAL,end_event):
    customs=Customs(env,num_police,time_consuming)
    customerNum=0
    while True:
        if CLIENT_INTERVAL==0:
            print("no customer :<")
        else:
            tmp=abs(random.normalvariate(CLIENT_INTERVAL,arrivalCV))
            intervalList.append(tmp)
            yield env.timeout(tmp)
            env.process(Client(env,'Client_%d'%customerNum,customs,customerNum))
            customerNum += 1


def declareSim():
    global env,end_event
    env=None
    end_event=None
    time.sleep(1)
    env = simpy.Environment()
    end_event = env.event()

def startSim():
    print("start simulation...")
    random.seed()
    env.process(setup(env, NUM_POLICE, TIME_CONSUMING, CLIENT_INTERVAL,end_event))
    env.run(until=end_event)
    print("simulation end")

def myajaxtestview(request):
    return HttpResponse(json.dumps("123"))

def myajaxtestview2(request):
    a = int(request.POST.get('test', None))
    if (a == len(resultList)):
        resultList.clear()
        return HttpResponse(json.dumps("END"))
    else:
        return HttpResponse(json.dumps(resultList[a]))


def runsim(request):
    declareSim()
    time.sleep(1)
    startSim()
    return HttpResponse(json.dumps("ok"))

def pausesim(request):
    global end_event
    status = int(request.POST.get('status', None))
    if(status==1):
        #如果要暫停
        end_event.succeed()
        end_event=None
        end_event=env.event()
        return HttpResponse(json.dumps("paused"))
    else:
        #如果要重啟
        env.run(until=end_event)
        return HttpResponse(json.dumps("run"))

def reset(request):
    resultList.clear()
    serviceList.clear()
    intervalList.clear()
    end_event.succeed()
    return HttpResponse(json.dumps("reseted"))

def retriveData(request):
    i = int(request.POST.get('i', None))
    return HttpResponse(json.dumps(resultList[i:]))

def passParameter(request):
    global CLIENT_INTERVAL,TIME_CONSUMING,arrivalCV,serviceTimeCV
    arrivalRate=float(request.POST.get('arrivalRate',None))
    serviceRate=float(request.POST.get('serviceRate',None))
    arrivalCV=200*float(request.POST.get('arrivalCV',None))
    serviceTimeCV=200*float(request.POST.get('serviceTimeCV',None))
    if arrivalRate==0:
        CLIENT_INTERVAL=0
    else:
        CLIENT_INTERVAL=int(10000-900*arrivalRate)
    if serviceRate==0:
        TIME_CONSUMING=0
    else:
        TIME_CONSUMING=int(10000-900*serviceRate)
    print("arrival time :"+str(CLIENT_INTERVAL)+" arrival CV:"+str(arrivalCV)+" service Rate:"+str(TIME_CONSUMING)+" service time cv:"+str(serviceTimeCV))
    return HttpResponse(json.dumps("parameter passed!!"))

def deleteTuple(request):
    delTuple = request.POST.get('mode', None)
    tuple.objects.get(title=delTuple).delete()
    return HttpResponse(json.dumps("deleted!!"))

def save(request):
    saveTuple = request.POST.get('mode', None)
    arrivalRate = float(request.POST.get('arrivalRate', None))
    serviceRate = float(request.POST.get('serviceRate', None))
    arrivalCV = float(request.POST.get('arrivalCV', None))
    serviceTimeCV = float(request.POST.get('serviceTimeCV', None))
    speed=int(request.POST.get('speed', None))
    tmp=tuple.objects.get(title=saveTuple)
    tmp.arrivalRate=arrivalRate
    tmp.serviceRate=serviceRate
    tmp.arrivalCV=arrivalCV
    tmp.serviceTimeCV=serviceTimeCV
    tmp.speed=speed
    tmp.save()
    return HttpResponse(json.dumps("saved!!"))

def saveAs(request):
    saveAsName = request.POST.get('saveAsName', None)
    arrivalRate = float(request.POST.get('arrivalRate', None))
    serviceRate = float(request.POST.get('serviceRate', None))
    arrivalCV = float(request.POST.get('arrivalCV', None))
    serviceTimeCV = float(request.POST.get('serviceTimeCV', None))
    speed = int(request.POST.get('speed', None))
    tmp=tuple.objects.get_or_create(title=saveAsName,arrivalRate=arrivalRate,serviceRate=serviceRate,arrivalCV=arrivalCV,serviceTimeCV=serviceTimeCV,speed=speed,predicted=1)
    print(tmp)
    if tmp[1] == True:
        return HttpResponse(json.dumps("saved as!!"))
    else:
        return HttpResponse(json.dumps("dupilcated name error!!"))

def terminate(request):
    print("terminate")
    end_event.succeed()
    intervalList.clear()
    arrivalList.clear()
    serviceList.clear()
    resultList.clear()
    adjustmentTime=0
    return HttpResponse(json.dumps("terminated!!"))

def getServiceTime(request):
    i = int(request.POST.get('i', None))
    return HttpResponse(json.dumps(serviceList[i:]))

def getClientInterval(request):
    i = int(request.POST.get('i', None))
    return HttpResponse(json.dumps(intervalList[i:]))

def checkArraySize(request):
    tmp = [len(intervalList),len(serviceList),len(resultList)]
    return HttpResponse(json.dumps(tmp))

def adjustArray(request):
    global adjustmentTime,arrivalList,env
    i = int(request.POST.get('i', None))
    adjustmentTime=env.now
    tmp=arrivalList[i]
    for j in range(i,len(arrivalList)):
        arrivalList[j]-=tmp
        print(j)
    return HttpResponse(json.dumps("OK"))