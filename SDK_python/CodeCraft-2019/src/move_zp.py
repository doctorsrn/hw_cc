#Version:0.0

import os
import sys
import copy
from collections import deque   #双端队列

#######windows下相对路径需要######
workpath=os.path.dirname(sys.argv[0])
os.chdir(workpath)          #指定py文件执行路径为当前工作路径



######数据结构定义######

#文件名
dirname=r'./config_0/'
carfile=dirname+r'car.txt'
crossfile=dirname+r'cross.txt'
roadfile=dirname+r'road.txt'
answerfile=dirname+r'answer.txt'


#定义车辆 路口 道路信息字典，即保存从txt读入信息
carmap={}
crossmap={}
roadmap={}
answermap={}


#处理后的数据形式
car_size=len(carmap)
cross_size=len(crossmap)
road_size=len(roadmap)

roadmat=[]    #路网模型
#-1 表示等待状态 -2 表示终止状态
waitstatus_now={}   #当前时刻等待上路车辆
movestatus_now={}   #当前时刻已上路车辆
#-1表示当前时刻车辆状态未变化 1表示当前时刻车辆状态已更新
carstatus_now={}


#时间定义
timeslice=-1  #时间变量
scheduletime=-1   #调度时间
movetime=-1   #行驶时间
excutetime=-1   #程序运行时间   


######函数实现######

def readdata(filename,mapname):
    #将txt信息保存到字典
    #ID号作为键，键值为其他剩余信息
    with open(filename,'r') as f :
        context=f.readlines()
##        print(context)
        for it in range(len(context)):
            line=context[it]
##            print(line)
            if line.find('#')!=-1 or line=='\n' or line==' ':continue
            else:
               linelist=line.split(')')[0].split('(')[-1].split(',')
               linelist=[int(i) for i in linelist]  
##               print(linelist)
               mapname[str(linelist[0])]=linelist[1:]
##               print(mapname)
##               input()


def createnvir(cross_size):
    #路网模型定义
    for i in range(cross_size):
        temp=[]
        for j in range(cross_size):
            temp.append({})      
        roadmat.append(temp)    
##    print(roadmat)
    for key in sorted(roadmap):
        channelnum=roadmap[key][2]
        row=roadmap[key][3]-1
        col=roadmap[key][4]-1     
        if roadmap[key][5]==1:              #单双向判断
            temp=[]
            for j in range(channelnum):
                temp.append(deque())
            roadmat[row][col][key]=temp
            roadmat[col][row][key]=copy.deepcopy(temp)   #深拷贝，否则出错
        else :
            temp=[]
            for j in range(channelnum):
                temp.append(deque())
            roadmat[row][col][key]=temp
##    print(roadmat)

def addcartolist():
    #将所有车辆加入 等待上路车辆 列表，并标记为 等待 状态
    #waitstatus_now 初始值为-3 carstatus_now初始值为0
    for key in sorted(carmap):
        waitstatus_now[key]=-3
        carstatus_now[key]=0
##    print(waitstatus_now)
##    print(carstatus_now)


def statusdisplay():
    #显示当前信息
    print("roadmat:")
    print(roadmat)
    print("waitstatus:")
    print(waitstatus_now)
    print("movestatus:")
    print(movestatus_now)
    print("carstatus:")
    print(carstatus_now)


def statusupdate(flag):
    #状态信息刷新
    if flag=='movestatus_now':
        for key in sorted(movestatus_now):
            movestatus_now[key]=-3
    elif flag=='carstatus_now':
        for key in sorted(carstatus_now):
            carstatus_now[key]=0
    else :
        print("flag error")
        pass
           

def depart():
    #发车
    for key in sorted(waitstatus_now):
        print(key)
        crossname=carmap[key][0]    
        roadname=str(answermap[key][1])

        row=roadmap[roadname][3]-1
        col=roadmap[roadname][4]-1

        if (row+1)==crossname:     #出发路口为road.txt起始点ID
            channelnum=len(roadmat[row][col][roadname])
            for i in range(channelnum):
                q=roadmat[row][col][roadname][i]
                if len(q)==0:   #前面车道上无车
                    speed=min(roadmap[roadname][1],carmap[key][1])  #当前车速为自身车速、道路限速最小值
                    postion=speed
                    precarid=str(-1);
                    carinfo=[key,crossname,roadname,speed,postion,precarid]
                    print(carinfo)
##                    print(roadmat)
##                    print(" ")
                    q.appendleft(carinfo)
                    print(roadmat)
                    waitstatus_now.pop(key)
                    movestatus_now[key]=-2  #将上路车辆标为终止状态
                    carstatus_now[key]=1
                    print(waitstatus_now)
                    print(movestatus_now)
                    print(carstatus_now)
                    break
                    
                else:      #前面车道上有车
                    [precarid,precross,precarroad,precarspeed,precarpos,precarpreid]=q.popleft()
                    if precarpos==1: continue
                    else :
                        speed=min(roadmap[roadname][1],carmap[key][1],carmap[precarid][1])  #当前车速为自身车速、道路限速最小值
                        postion=min(speed,precarpos-1)
                        carinfo=[key,crossname,roadname,speed,postion,precarid]
                        print(carinfo)
                        q.appendleft([precarid,precross,precarroad,precarspeed,precarpos,precarpreid])
##                        print(roadmat)
##                        print(" ")
                        q.appendleft(carinfo)
                        print(roadmat)
                        waitstatus_now.pop(key)
                        movestatus_now[key]=-2  #将上路车辆标为终止状态
                        carstatus_now[key]=1
                        print(waitstatus_now)
                        print(movestatus_now)
                        print(carstatus_now)
                        break
                                                        

        else:         #出发路口为road.txt终点ID
            row=roadmap[roadname][4]-1
            col=roadmap[roadname][3]-1            
            channelnum=len(roadmat[row][col][roadname])
            for i in range(channelnum):
                q=roadmat[row][col][roadname][i]
                if len(q)==0:   #前面车道上无车
                    speed=min(roadmap[roadname][1],carmap[key][1])  #当前车速为自身车速、道路限速最小值
                    postion=speed
                    precarid=str(-1);
                    carinfo=[key,crossname,roadname,speed,postion,precarid]
                    print(carinfo)
##                    print(roadmat)
##                    print(" ")
                    q.appendleft(carinfo)
                    print(roadmat)
                    waitstatus_now.pop(key)
                    movestatus_now[key]=-2  #将上路车辆标为终止状态
                    carstatus_now[key]=1
                    print(waitstatus_now)
                    print(movestatus_now)
                    print(carstatus_now)
                    break
                    
                else:      #前面车道上有车
                    [precarid,precross,precarroad,precarspeed,precarpos,precarpreid]=q.popleft()
                    if precarpos==1: continue
                    else :
                        speed=min(roadmap[roadname][1],carmap[key][1],carmap[precarid][1])  #当前车速为自身车速、道路限速最小值
                        postion=min(speed,precarpos-1)
                        carinfo=[key,crossname,roadname,speed,postion,precarid]
                        print(carinfo)
                        q.appendleft([precarid,precross,precarroad,precarspeed,precarpos,precarpreid])
##                        print(roadmat)
##                        print(" ")
                        q.appendleft(carinfo)
                        print(roadmat)
                        waitstatus_now.pop(key)
                        movestatus_now[key]=-2  #将上路车辆标为终止状态
                        carstatus_now[key]=1
                        print(waitstatus_now)
                        print(movestatus_now)
                        print(carstatus_now)
                        break
                
    statusdisplay()        
    statusupdate('carstatus_now')
    statusupdate('movestatus_now')
        


def carscan(cross_size):
    #车辆遍历，标记 等待 或终止
    for i in range(cross_size):
        for j in range(cross_size):
            if roadmat[i][j]=={} :continue
            else:
                roadname=list(roadmat[i][j].keys())[0]
                roadlength=roadmap[roadname][0]
                channelnum=len(roadmat[i][j][roadname])
                for k in range(channelnum):
                    q=roadmat[i][j][roadname][k]
                    carnum=len(q)
                    if carnum==0:   #当前车道无车
                        continue
                    else :                        
                        for m in range(carnum):
                            index=carnum-m-1
                            print(q[index])                           
                            #[carid,cross_last,carroad,carspeed,carpos,precarid]=q.pop()
                            [carid,cross_last,carroad,carspeed,carpos,precarid]=q[index]    #从该车道最前方车辆开始遍历
                            if precarid=='-1':  #有无前车阻挡                                
                                if carpos+carspeed>roadlength:      #是否出路口                            
                                    movestatus_now[carid]=-1
                                    carstatus_now[carid]=1
                                else:
                                    carpos+=carspeed
                                    q[index][4]=carpos
                                    carstatus_now[carid]=1
##                                    carinfo=[carid,cross_last,carroad,carspeed,carpos,precarid]
##                                    print(carinfo)
##                                    q.append(carinfo)
                            else:
                                [precarid,precross_last,precarroad,precarspeed,precarpos,preprecarid]=q[index+1]
                                if movestatus_now[precarid]== -1 and carstatus_now[precarid]==1:        #前车是否为等待状态
                                    movestatus_now[carid]=-1
                                    carstatus_now[carid]=1
                                else:
                                    carspeed=min(carspeed,precarpos-carpos)
                                    carpos+=carspeed
                                    q[index][4]=carpos
                                    carstatus_now[carid]=1

    statusdisplay()                                
    statusupdate('carstatus_now')                        
            

def crossupdate():
    #路口更新
    pass

def roadupdate():
    #道路内部更新
    pass

    
    

def main():
    readdata(carfile,carmap)
#    print(carmap)
    readdata(roadfile,roadmap)
##    print(roadmap)
    readdata(crossfile,crossmap)
#    print(crossmap)

#######路径规划######


######调度######
    car_size=len(carmap)
    cross_size=len(crossmap)
    road_size=len(roadmap)
    
    readdata(answerfile,answermap)
##    print(answermap)
    
    #路网定义
    createnvir(cross_size)
    
    #将所有车放入等待上路集合中
    addcartolist()

    #开始调度
    print(roadmat)
    print(waitstatus_now)
    print(carstatus_now)


    depart() #发车
    
    carscan(cross_size)  #各道路车辆扫描标记

if __name__=="__main__":
    main()
