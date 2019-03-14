#Version:0.11

import os
import sys
import copy
from collections import deque   #双端队列
import profile
import time

#######windows下相对路径需要######
workpath=os.path.dirname(sys.argv[0])
os.chdir(workpath)          #指定py文件执行路径为当前工作路径



######数据结构定义######

#文件名
dirname=r'../config_0/'
carfile=dirname+r'car.txt'
crossfile=dirname+r'cross.txt'
roadfile=dirname+r'road.txt'
answerfile=dirname+r'answer.txt'


#定义车辆 路口 道路信息字典，即保存从txt读入信息
carmap={}
crossmap={}
roadmap={}
answermap={}
crossidmap={}  #存放路口id 与0,1,2,3..的对应关系

#处理后的数据形式
car_size=len(carmap)
cross_size=len(crossmap)
road_size=len(roadmap)

roadmat=[]    #路网模型

#状态信息定义
#-1 表示等待状态 -2 表示终止状态
waitstatus_now={}   #当前时刻等待上路车辆
movestatus_now={}   #当前时刻已上路车辆
#-1表示当前时刻车辆状态未变化 1表示当前时刻车辆状态已更新
carstatus_now={}
carstatus_last={}  #上一时刻车辆状态
scheduleover=0     #调度结束标志，0 未结束 1结束
lockflag=0  #死锁标志 0 未发生死锁 1 发生死锁

#时间定义
timeslice=0  #时间变量
scheduletime=0   #调度时间
movetime={}   #行驶时间
excutetime=0   #程序运行时间   



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
               mapname[linelist[0]]=linelist[1:]
##               print(mapname)
##               input()
##        print(filename)
        if filename.split('/')[-1].split('.')[0]=='cross':
            temp=0
            for key in sorted(mapname):
                mapname[key].append(temp)   #为crossmap增加一列顺序号
                temp+=1
                
def crossidtransfer(crossmap,crossidmap):
    for key in crossmap:
        newkey=crossmap[key][-1]
##        print(newkey)
        crossidmap[newkey]=key


def createnvir(cross_size):
    #路网模型定义
    for i in range(cross_size):
        temp=[]
        for j in range(cross_size):
            temp.append({})      
        roadmat.append(temp)    
##    print(roadmat)
    for key in sorted(roadmap):
##        print(key)
        channelnum=roadmap[key][2]
        row=crossmap[roadmap[key][3]][-1]
        col=crossmap[roadmap[key][4]][-1]     
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
    print("timeslice:")
    print(timeslice)
    print("roadmat:")
##    print(roadmat)
    print("answer:")
    print(answermap)
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
    #每一个车辆为一个列表  {车ID，已过路口，当前道路ID，当前车速，当前位置，前车ID}
    for key in sorted(waitstatus_now):
        if answermap[key][0]>timeslice:continue   #大于当前出发时间的不考虑
##        print(key)
        crossname=carmap[key][0]    
        roadname=answermap[key][1]

        row=crossmap[roadmap[roadname][3]][-1]
        col=crossmap[roadmap[roadname][4]][-1]

        if row==crossmap[crossname][-1]:     #出发路口为road.txt起始点ID
            channelnum=len(roadmat[row][col][roadname])
            for channelorder in range(channelnum):
                q=roadmat[row][col][roadname][channelorder]
                if len(q)==0:   #前面车道上无车
                    speed=min(roadmap[roadname][1],carmap[key][1])  #当前车速为自身车速、道路限速最小值
                    postion=speed
                    precarid=str(-1);
                    carinfo=[key,crossname,roadname,speed,postion,precarid]
##                    print(carinfo)
                    q.appendleft(carinfo)
##                    print(roadmat)
                    waitstatus_now.pop(key)
                    movestatus_now[key]=-2  #将上路车辆标为终止状态
                    carstatus_now[key]=1
##                    print(waitstatus_now)
##                    print(movestatus_now)
##                    print(carstatus_now)
                    break
                    
                else:      #前面车道上有车
                    [precarid,precross,precarroad,precarspeed,precarpos,precarpreid]=q.popleft()
                    if precarpos==1: continue
                    else :
                        speed=min(roadmap[roadname][1],carmap[key][1],carmap[precarid][1])  #当前车速为自身车速、道路限速最小值
                        postion=min(speed,precarpos-1)
                        carinfo=[key,crossname,roadname,speed,postion,precarid]
##                        print(carinfo)
                        q.appendleft([precarid,precross,precarroad,precarspeed,precarpos,precarpreid])
                        q.appendleft(carinfo)
##                        print(roadmat)
                        waitstatus_now.pop(key)
                        movestatus_now[key]=-2  #将上路车辆标为终止状态
                        carstatus_now[key]=1
##                        print(waitstatus_now)
##                        print(movestatus_now)
##                        print(carstatus_now)
                        break
                                                        

        else:         #出发路口为road.txt终点ID
            row=crossmap[roadmap[roadname][4]][-1]
            col=crossmap[roadmap[roadname][3]][-1]           
            channelnum=len(roadmat[row][col][roadname])
            for channelorder in range(channelnum):
                q=roadmat[row][col][roadname][channelorder]
                if len(q)==0:   #前面车道上无车
                    speed=min(roadmap[roadname][1],carmap[key][1])  #当前车速为自身车速、道路限速最小值
                    postion=speed
                    precarid=str(-1);
                    carinfo=[key,crossname,roadname,speed,postion,precarid]
##                    print(carinfo)
                    q.appendleft(carinfo)
##                    print(roadmat)
                    waitstatus_now.pop(key)
                    movestatus_now[key]=-2  #将上路车辆标为终止状态
                    carstatus_now[key]=1
##                    print(waitstatus_now)
##                    print(movestatus_now)
##                    print(carstatus_now)
                    break
                    
                else:      #前面车道上有车
                    [precarid,precross,precarroad,precarspeed,precarpos,precarpreid]=q.popleft()
                    if precarpos==1: continue
                    else :
                        speed=min(roadmap[roadname][1],carmap[key][1],carmap[precarid][1])  #当前车速为自身车速、道路限速最小值
                        postion=min(speed,precarpos-1)
                        carinfo=[key,crossname,roadname,speed,postion,precarid]
##                        print(carinfo)
                        q.appendleft([precarid,precross,precarroad,precarspeed,precarpos,precarpreid])
                        q.appendleft(carinfo)
##                        print(roadmat)
                        waitstatus_now.pop(key)
                        movestatus_now[key]=-2  #将上路车辆标为终止状态
                        carstatus_now[key]=1
##                        print(waitstatus_now)
##                        print(movestatus_now)
##                        print(carstatus_now)
                        break
                
##    statusdisplay()     #发车完毕显示状态   
        


def carscan(cross_size):
    #车辆遍历，标记 等待 或终止
    for row in range(cross_size):
        for col in range(cross_size):
            if roadmat[row][col]=={} :continue
            else:
                roadname=list(roadmat[row][col].keys())[0]
                roadlength=roadmap[roadname][0]
                channelnum=len(roadmat[row][col][roadname])
                for pos in range(roadlength):
                    for k in range(channelnum):
                        q=roadmat[row][col][roadname][k]
                        carnum=len(q)
                        if carnum==0:   #当前车道无车
                            continue
                        else :                        
                            for m in range(carnum):
                                index=carnum-m-1
##                                print(q[index])                           
                                [carid,cross_last,carroad,carspeed,carpos,precarid]=q[index]    #从该车道最前方车辆开始遍历
                                if carpos!=(roadlength-pos):continue
                                if precarid=='-1':  #有无前车阻挡                                
                                    if carpos+carspeed>roadlength:      #是否出路口
                                        movestatus_now[carid]=-1

                                    else:
                                        carpos+=carspeed
                                        q[index][4]=carpos
                                        movestatus_now[carid]=-2
                                        carstatus_now[carid]=1

                                else:
                                    [precarid,precross_last,precarroad,precarspeed,precarpos,preprecarid]=q[index+1]
                                    if movestatus_now[precarid]== -1:        #前车是否为等待状态
                                        movestatus_now[carid]=-1

                                    else:
                                        carspeed=min(carspeed,precarpos-carpos)
                                        carpos+=carspeed
                                        q[index][4]=carpos
                                        movestatus_now[carid]=-2
                                        carstatus_now[carid]=1

##    statusdisplay()      #标记完毕显示状态                                                
            
def turndir(carid,carroad_now,cross_now):
    #拐弯方向判定
    #直行 1 左拐 2 右拐 3
    #carid 车辆ID carroad_now 所在道路 cross_now 所要通过路口
    plan=answermap[carid]
    if len(plan)==2:    #路线列表长度为2且要通过路口时即到达目的地
        return [1,'-1']
    road_next=-1
    for i in range(len(plan)):
        if plan[i]==1:continue
        else :
            road_next=plan[i+1]
            break
    crossinfo=crossmap[cross_now]
    lastindex=-1
    nextindex=-1
    for i in range(len(crossinfo)):
        road=crossinfo[i]
        if road==carroad_now:
            lastindex=i
        elif road==road_next:
            nextindex=i
        else:
            pass
    if abs(nextindex-lastindex)==2:
        return [1,road_next]
    elif abs(nextindex-lastindex)==1:
        if nextindex>lastindex:return [2,road_next]
        else: return [3,road_next]
    elif abs(nextindex-lastindex)==3:
        if nextindex<lastindex:return [2,road_next]
        else: return [3,road_next]
    

def swap(ll,index1,index2):
    temp=ll[index1]
    ll[index1]=ll[index2]
    ll[index2]=temp



def crossupdate(cross_size):
    #路口更新
    for col in range(cross_size):
        #首先将要通过该路口的所有车辆信息存入
        crossname=crossidmap[col]
        crossroad=crossmap[crossname]
        if -1 in crossroad:
            crossroad.remove(-1)   #去除-1
        crossroad=sorted(crossroad)
        crossroadnum=len(crossroad)
        index=0
        while index!=-1:
            firstroad=crossroad[index]
                  
            tempdict={} #存放各道路优先权最高的车辆
            for row in range(cross_size):
                if roadmat[row][col]=={} :continue
                else:                
                    roadname=list(roadmat[row][col].keys())[0]
                    channelnum=len(roadmat[row][col][roadname])
                    roadlength=roadmap[roadname][0]
                    for pos in range(roadlength):
                        findflag=0
                        for channelorder in range(channelnum):
                            q=roadmat[row][col][roadname][channelorder]     #检查该道路上优先权最高的车辆
                            carnum=len(q)
                            if carnum==0:continue   #当前车道上无车
                            else:
                                [carid,cross_last,carroad,carspeed,carpos,precarid]=q[carnum-1]
                                if carpos!=(roadlength-pos):continue   #不是当前检查位置换车道
                                if movestatus_now[carid]==-1:
                                    if (carpos+carspeed)>roadlength:
                                        [dirflag,nextroad]=turndir(carid,carroad,crossname)
                                        if nextroad=='-1':    #已到达目的地
                                            q.pop()
                                            movestatus_now.pop(carid)
                                            carstatus_now.pop(carid)
                                            movetime[carid]=timeslice-answermap[carid][0]+1
                                        else:
                                            tempdict[roadname]=[carid,row,col,crossname,roadname,channelorder,dirflag,nextroad]       #[车辆ID，当前路口x,当前路口y，所在路口，所在道路，所在车道，车辆转弯状态，下一条道路]
                                            findflag=1
                                            break
                                    else:
                                        pass
                                else :
                                    pass
                        if findflag==1:break
##            print("cross:")
##            print(crossname)
##            print(tempdict)
            if tempdict=={}:
                index=-1
                break     #当前路口没有要出的车辆退出
            
            order=[]   #路口车辆调度优先级
            #对于该路口的每一条道路车辆分别进行处理，首先确定调度优先级
            if firstroad in list(tempdict.keys()):
                goalroad=tempdict[firstroad][-1]
                for roadname in sorted(tempdict):
                    if tempdict[roadname][-1]!=goalroad:continue       #去除非同一目标道路
                    else:
                        order.append(roadname)

                ordernum=len(order)
                for m in range(ordernum-1):   #冒泡排序确定优先级顺序
                    for n in range(ordernum-m-1):
                        if m==n :continue
                        else:
                            road1=order[m]
                            road2=order[n]                    
                            if tempdict[road1][-2]<tempdict[road2][-1]:
                                if m<n:pass
                                else:swap(order,m,n)
                            else:
                                if m<n:swap(order,m,n)
                                else:pass                            
                        
##                print("order:")
##                print(order)

                if order[0]!=firstroad:    #如果最高优先级不是当前拥有调度权的道路，则失去调度权
                    index+=1
                else:                
                    [carid,roadmatx,roadmaty,crossname,roadname,carchannel,dirflag,nextroad]=tempdict[firstroad]
                    q_last=roadmat[roadmatx][roadmaty][roadname][carchannel]    #要过路口的车道队列
                    row=crossmap[roadmap[nextroad][3]][-1]
                    col=crossmap[roadmap[nextroad][4]][-1]
                    if crossidmap[row]==crossname:
                        roadmatx_next=row
                        roadmaty_next=col
                    else:
                        roadmatx_next=col
                        roadmaty_next=row
                    channelnum=len(roadmat[roadmatx_next][roadmaty_next][nextroad])
                    roadlength_last=roadmap[roadname][0]
                    roadlength_next=roadmap[nextroad][0]
                    for channelorder in range(channelnum):
                        q=roadmat[roadmatx_next][roadmaty_next][nextroad][channelorder]
                        carnum=len(q)
                        if carnum==0:   #当前车道无车
                            [precarid,precross_last,precarroad,precarspeed,precarpos,preprecarid]=q_last.pop()
                            s_left=precarspeed+precarpos-roadmap[precarroad][0]    #前段道路剩余理论待行驶距离
                            speed_next=min(carmap[precarid][2],roadmap[nextroad][1])
                            if s_left<=speed_next:
                                q.appendleft([precarid,crossname,nextroad,speed_next,s_left,'-1'])
                                carnum_last=len(q_last)
                                if carnum_last!=0:
                                    q_last[carnum_last-1][-1]='-1'
                                answermap[precarid].remove(precarroad)
                                movestatus_now[precarid]=-2
                                carstatus_now[precarid]=1
                                break
                            else :
                                q_last.append([precarid,precross_last,precarroad,precarspeed,roadlength_last,preprecarid])
                                movestatus_now[precarid]=-2
                                carstatus_now[precarid]=1
                                break
                        elif  carnum==roadlength_next:     #该车道满换一车道
                            continue
                        else:
                            [nextcarid,nextcross_last,nextcarroad,nextcarspeed,nextcarpos,nextprecarid]=q[0]    #查询前一车道最后一个车的信息
                            [precarid,precross_last,precarroad,precarspeed,precarpos,preprecarid]=q_last.pop()
                            s_left=precarspeed+precarpos-roadmap[precarroad][0]    #前段道路剩余理论待行驶距离
                            speed_next=min(carmap[precarid][2],roadlength_next)
                            if s_left<=speed_next:     #是否超过下条道路最大行驶距离
                                if s_left<nextcarpos:    #是否超过前车
                                    q.appendleft([precarid,crossname,nextroad,speed_next,s_left,nextcarid])
                                    carnum_last=len(q_last)
                                    if carnum_last!=0:
                                        q_last[carnum_last-1][-1]='-1'
                                    answermap[precarid].remove(precarroad)
                                    movestatus_now[precarid]=-2
                                    carstatus_now[precarid]=1
                                    break
                                else:
                                    if nextcarpos!=1:            #考虑前车是否在道路最后排
                                        q.appendleft([precarid,crossname,nextroad,speed_next,nextcarpos-1,nextcarid])
                                        carnum_last=len(q_last)
                                        if carnum_last!=0:
                                            q_last[carnum_last-1][-1]='-1'
                                        answermap[precarid].remove(precarroad)
                                        movestatus_now[precarid]=-2
                                        carstatus_now[precarid]=1
                                        break
                                    else:
                                        q_last.append([precarid,precross_last,precarroad,precarspeed,roadlength_last,preprecarid])
                                        movestatus_now[precarid]=-2
                                        carstatus_now[precarid]=1
                                        break 
                            else:
                                q_last.append([precarid,precross_last,precarroad,precarspeed,roadlength_last,preprecarid])
                                movestatus_now[precarid]=-2
                                carstatus_now[precarid]=1
                                break                
            else:
                index+=1
            
                             
            if index==crossroadnum:index=0        #循环
        

##    statusdisplay()   #路口更新结束显示状态     

def roadupdate(cross_size):
    #道路内部更新
    for row in range(cross_size):
        for col in range(cross_size):
            if roadmat[row][col]=={} :continue
            else:
                roadname=list(roadmat[row][col].keys())[0]
                roadlength=roadmap[roadname][0]
                channelnum=len(roadmat[row][col][roadname])
                for pos in range(roadlength):
                    for channelorder in range(channelnum):
                        q=roadmat[row][col][roadname][channelorder]
                        carnum=len(q)
                        if carnum==0:   #当前车道无车
                            continue
                        else :                        
                            for m in range(carnum):
                                index=carnum-m-1
##                                print(q[index])                           
                                [carid,cross_last,carroad,carspeed,carpos,precarid]=q[index]    #从该车道最前方车辆开始遍历
                                if carpos!=(roadlength-pos):continue   #不是当前检查位置换车道
                                if carstatus_now[carid]==1:
                                    continue
                                else:
                                    if precarid=='-1':  #有无前车阻挡                                
                                        if carpos+carspeed>roadlength:      #是否出路口
                                            pass
                                        else:
                                            carpos+=carspeed
                                            q[index][4]=carpos
                                            movestatus_now[carid]=-2
                                            carstatus_now[carid]=1
                                    else:
                                        [precarid,precross_last,precarroad,precarspeed,precarpos,preprecarid]=q[index+1]
                                        if movestatus_now[precarid]== -1:        #前车是否为等待状态
                                            pass
                                        else:
                                            carspeed=min(carspeed,precarpos-carpos)
                                            carpos+=carspeed
                                            q[index][4]=carpos
                                            movestatus_now[carid]=-2
                                            carstatus_now[carid]=1

##    statusdisplay()         #道路内部更新结束显示状态                       

def dictcmp(dict1,dict2):    #字典比较，相等为1 不等为0
    for key in dict1:
        if key not in dict2:
            return 0
        elif dict1[key]==dict2[key]:
            continue
        else:
            return 0
    return 1
    
def CalScheduleTime(answerfile,crossmap,crossidmap,roadmap,carmap,cross_size,road_size,car_size,roadmat):
    
    begintime=time.time()    
    
    readdata(answerfile,answermap)
##    print(answermap)
    
    #将所有车放入等待上路集合中
    addcartolist()

    #开始调度
    print(roadmat)
    print(waitstatus_now)
    print(carstatus_now)

    #[dir,next]=turndir('1001','509','12')

    global timeslice
    global scheduleover
    global carstatus_last
    global lockflag
    while scheduleover!=1:
                
        carscan(cross_size)

        tempcopy=carstatus_now
        carstatus_last=tempcopy.copy()

        scanover=0
        for key in carstatus_last:
            if carstatus_last[key]==0:
                scanover=1
                break

        if scanover==1:
            updateflag=0     #临时标志 0 路口、道路内未更新完  1更新结束
            while updateflag!=1:
                if waitstatus_now=={} and movestatus_now=={} and timeslice!=0:
                    scheduleover=1       #待发车和已上路集合都为空时，调度结束
                    break
                for key in sorted(carstatus_now):
                    if carstatus_now[key]==0:
                        if  movestatus_now=={}:
                            updateflag=1
                            break
                        elif movestatus_now[key]==-2:
                            updateflag=1
                        else:
                            updateflag=0
                            break
                    else:
                        updateflag=1

                if updateflag==0:
                    crossupdate(cross_size)
                    roadupdate(cross_size)


            if dictcmp(carstatus_last,carstatus_now) and movestatus_now!={}:     #判断是否出现死锁
                scheduleover=1
                lockflag=1
                break
        else:
            pass
            
        depart()            

        statusdisplay()
        timeslice+=1
        statusupdate('carstatus_now')
        statusupdate('movestatus_now')
            
    endtime=time.time()
    excutetime=endtime-begintime
    print("excutetime: ")
    print(excutetime)
    if not lockflag:
        scheduletime=timeslice
    else:
        scheduletime=-1
    print("scheduletime: ")
    print(scheduletime)
    print("car movetime:")
    print(movetime)
    
    return scheduletime

def main():
    
    readdata(carfile,carmap)
##    print(carmap)
    readdata(roadfile,roadmap)
##    print(roadmap)
    readdata(crossfile,crossmap)
##    print(crossmap)
    crossidtransfer(crossmap,crossidmap)
##    print(crossidmap)
    car_size=len(carmap)
    cross_size=len(crossmap)
    road_size=len(roadmap)

    #路网定义
    createnvir(cross_size)

    
#######路径规划######


######调度######

    #参数：answer.txt路径、路口字典、路口id对应关系字典、道路字典、车辆字典、路口数目、道路数目、车辆数目、路网
    CalScheduleTime(answerfile,crossmap,crossidmap,roadmap,carmap,cross_size,road_size,car_size,roadmat)   



if __name__=="__main__":
    profile.run('main()')
