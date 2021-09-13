import random
import simpy

#參數初始化
RANDOM_SEED=0
NUM_POLICE=1
TIME_CONSUMING=150 #處理時間
CLIENT_INTERVAL=100 #顧客間隔
SIM_TIME=1000 #模擬時間


class Customs(object):
    #海關
    def __init__(self,env,num_police,time_consuming):
        self.env=env
        self.police=simpy.Resource(env,num_police)
        self.time_consuming=time_consuming
        self.allClient=0
        self.accomplishClient=0

    def processing(self,client):
        yield self.env.timeout(random.randint(self.time_consuming-150,self.time_consuming+150))
        self.allClient+=1
        self.accomplishClient+=1
        print("目前服務用戶數:%d , 已完成用戶數:%.2f"%(self.allClient,self.accomplishClient))

def Client(env,name,customs):
    print("%s 到達海關 at %.2f" %(name,env.now))
    with customs.police.request() as request:
        yield request
        print('%s 接受檢查   at %.2f.' % (name, env.now))
        yield env.process(customs.processing(name))
        print('%s 離開海關 at %.2f.' % (name, env.now))

def setup(env,num_police,time_consuming,client_interval):
    customs=Customs(env,num_police,time_consuming)
    i=0
    while True:
        yield env.timeout(random.randint(client_interval-2,client_interval+3))
        i +=1
        env.process(Client(env,'Client_%d'%i,customs))

print("start simulation...")
random.seed()

env=simpy.Environment()
env.process(setup(env,NUM_POLICE,TIME_CONSUMING,CLIENT_INTERVAL))

env.run(until=SIM_TIME)

