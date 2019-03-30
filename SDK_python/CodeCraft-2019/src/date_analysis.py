# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:57:31 2019

@author: Srn
"""

from IOModule import read_from_txt
import matplotlib.pyplot as plt


rpath = '../config0'
cross_path = rpath + '/cross.txt'
road_path = rpath + '/road.txt'
car_path = rpath + '/car.txt'
answer_path = rpath + '/answer.txt'

cross_df = read_from_txt(cross_path)
print(cross_df.head())
print(cross_df.shape)

road_df = read_from_txt(road_path)
print(road_df.head())
print(road_df.shape)

car_df = read_from_txt(car_path)
print(car_df.head())
print(car_df.shape)


# 对道路进行数据分析
plt.figure(1, figsize=(6, 12))
#第一行第一列图形
ax1 = plt.subplot(4,2,1)
#第一行第二列图形
ax2 = plt.subplot(4,2,2)
#第二行
ax3 = plt.subplot(4,2,3)

ax4 = plt.subplot(4,2,4)
ax5 = plt.subplot(4,2,5)
ax6 = plt.subplot(4,2,6)
ax7 = plt.subplot(4,2,7)

# 设置子图间距
plt.tight_layout(1.5, 1.5, 1.5)
plt.subplots_adjust(wspace =0.3, hspace =0.6)
plt.sca(ax1)
road_df['speed'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('road speed distribution')
plt.xlabel('max speed')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax2)
road_df['channel'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('channel distribution')
plt.xlabel('channel')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)


plt.sca(ax3)
road_df['from'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('from distribution')
plt.xlabel('from')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax4)
road_df['to'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('to distribution')
plt.xlabel('to')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax5)
road_df['isDuplex'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('isDuplex distribution')
plt.xlabel('isDuplex')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

road_df['time'] = road_df.apply(lambda x: (x['length'] / x['speed']), axis=1)
plt.sca(ax6)
road_df['time'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('time cost distribution')
plt.xlabel('time cost')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax7)
road_df['length'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('length distribution')
plt.xlabel('length cost')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)


# 对路口进行分析
cross_df['count'] = (cross_df < 0).sum(axis=1)

plt.figure(2)
cross_df['count'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('cross -1 distribution')
plt.xlabel('count df < 0')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)


## 对车辆数据进行分析
plt.figure(3, figsize=(6, 8))
#第一行第一列图形
ax1 = plt.subplot(3,2,1)
#第一行第二列图形
ax2 = plt.subplot(3,2,2)
#第二行
ax3 = plt.subplot(3,2,3)
ax4 = plt.subplot(3,2,4)
ax5 = plt.subplot(3,2,5)
ax6 = plt.subplot(3,2,6)

#统计车辆起始站点间路口数
car_df['distance'] = car_df.apply(lambda x: abs(x['to'] - x['from']), axis=1)

# 设置子图间距
plt.tight_layout(1.5, 1.5, 1.5)
plt.subplots_adjust(wspace =0.3, hspace =0.6)

plt.sca(ax1)
car_df['from'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('from distribution')
plt.xlabel('from')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax2)
car_df['to'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('to distribution')
plt.xlabel('to')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax3)
car_df['speed'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('speed distribution')
plt.xlabel('max speed')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax4)
car_df['planTime'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('planTime distribution')
plt.xlabel('planTime')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax5)
car_df['distance'].plot.hist(grid=True, bins=20, rwidth=0.9,
     color='#607c8e')
plt.title('distance distribution')
plt.xlabel('distance')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)

plt.sca(ax6)
plt.scatter(list(car_df['from']), list(car_df['to']))
plt.title('car from-to distribution')
plt.xlabel('car from')
plt.ylabel('car to')


## 对车辆数据进行分析
plt.figure(4, figsize=(6, 8))
#第一行第一列图形
ax1 = plt.subplot(3,2,1)
#第一行第二列图形
ax2 = plt.subplot(3,2,2)
#第二行
ax3 = plt.subplot(3,2,3)
ax4 = plt.subplot(3,2,4)
ax5 = plt.subplot(3,2,5)
ax6 = plt.subplot(3,2,6)

car_df_sort = car_df.sort_values(by=['speed', 'id'], axis=0, ascending=[False, True])
car_max_speed = car_df_sort.loc[car_df_sort['speed'] > 7]
# #统计车辆起始站点间路口数
# car_df['distance'] = car_df.apply(lambda x: abs(x['to'] - x['from']), axis=1)

# 设置子图间距
plt.tight_layout(1.5, 1.5, 1.5)
plt.subplots_adjust(wspace =0.3, hspace =0.6)

plt.sca(ax1)
plt.scatter(list(car_max_speed['from']), list(car_max_speed['to']))
plt.title('max speed from-to distribution')
plt.xlabel('car from')
plt.ylabel('car to')
plt.show()