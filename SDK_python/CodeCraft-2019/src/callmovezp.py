import os
import sys
from move_zp import *

#######windows下相对路径需要######
workpath=os.path.dirname(sys.argv[0])
os.chdir(workpath)          #指定py文件执行路径为当前工作路径



#文件名
dirname=r'../config_0/'
carfile=dirname+r'car.txt'
crossfile=dirname+r'cross.txt'
roadfile=dirname+r'road.txt'
answerfile=dirname+r'answer.txt'


def main():
    #读数据
    readdata(carfile,carmap)
    readdata(roadfile,roadmap)
    readdata(crossfile,crossmap)
    crossidtransfer(crossmap,crossidmap)
    car_size=len(carmap)
    cross_size=len(crossmap)
    road_size=len(roadmap)

    #路网定义
    createnvir(cross_size)

    #求调度时间
    value=CalScheduleTime(answerfile,crossmap,crossidmap,roadmap,carmap,cross_size,road_size,car_size,roadmat)   #参数：answer.txt路径、路口字典、道路字典、车辆字典、路口数目、道路数目、车辆数目、路网
    print(value)
    
# if __name__=="__main__":
#     main()
