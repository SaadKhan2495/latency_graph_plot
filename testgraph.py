import sys
import os
import decimal
import matplotlib.pyplot as plt
import numpy as np
import math

file_name = sys.argv[1]
x_axis=[]
y_axis=[]

with open(file_name,'r') as in_file, open('sorted_'+file_name,'w') as out_file:
    for each_line in in_file:
        temp=each_line.split(',')
        x_axis.append(float(temp[0]))
        y_axis.append(float(temp[1]))

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)

plt.xlabel("Percentile(%)")
plt.ylabel("Time (microseconds)")
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.xticks([0,5,9,18,27,36,45,54,60],
           ['Min',50,90,99,99.9,99.99,99.999,99.9999,'Max'],rotation=90)
plt.yticks([1000,2000,3000,4000,5000],
           [1,2,3,4,5],rotation=0)

ax.set_yticks([y_axis[5],y_axis[9],y_axis[18],y_axis[27],y_axis[36],y_axis[45],y_axis[54],y_axis[60]],minor=True)
ax.set_yticklabels([y_axis[5]/1000,y_axis[9]/1000,y_axis[18]/1000,y_axis[27]/1000,y_axis[36]/1000,y_axis[45]/1000,y_axis[54]/1000,y_axis[60]/1000],minor=True)
plt.tick_params(which='minor',axis='y',labelsize=6)
plt.tick_params(which='major',axis='both',width=1.75,length=5)
plt.tick_params(which='minor',axis='both',width=1.25)

line1_vertical_start=[5,5]
line1_vertical_end=[0,y_axis[5]]
ax.plot(line1_vertical_start,line1_vertical_end,color="gray",linestyle=':')
line1_horizontal_start=[0,5]
line1_horizontal_end=[y_axis[5],y_axis[5]]
ax.plot(line1_horizontal_start,line1_horizontal_end,color="gray",linestyle=':')

line2_vertical_start=[18,18]
line2_vertical_end=[0,y_axis[18]]
ax.plot(line2_vertical_start,line2_vertical_end,color="gray",linestyle=':')
line2_horizontal_start=[0,18]
line2_horizontal_end=[y_axis[18],y_axis[18]]
ax.plot(line2_horizontal_start,line2_horizontal_end,color="gray",linestyle=':')

line3_vertical_start=[27,27]
line3_vertical_end=[0,y_axis[27]]
ax.plot(line3_vertical_start,line3_vertical_end,color="gray",linestyle=':')
line3_horizontal_start=[0,27]
line3_horizontal_end=[y_axis[27],y_axis[27]]
ax.plot(line3_horizontal_start,line3_horizontal_end,color="gray",linestyle=':')

line4_vertical_start=[36,36]
line4_vertical_end=[0,y_axis[36]]
ax.plot(line4_vertical_start,line4_vertical_end,color="gray",linestyle=':')
line4_horizontal_start=[0,36]
line4_horizontal_end=[y_axis[36],y_axis[36]]
ax.plot(line4_horizontal_start,line4_horizontal_end,color="gray",linestyle=':')

line5_vertical_start=[45,45]
line5_vertical_end=[0,y_axis[45]]
ax.plot(line5_vertical_start,line5_vertical_end,color="gray",linestyle=':')
line5_horizontal_start=[0,45]
line5_horizontal_end=[y_axis[45],y_axis[45]]
ax.plot(line5_horizontal_start,line5_horizontal_end,color="gray",linestyle=':')

line6_vertical_start=[54,54]
line6_vertical_end=[0,y_axis[54]]
ax.plot(line6_vertical_start,line6_vertical_end,color="gray",linestyle=':')
line6_horizontal_start=[0,54]
line6_horizontal_end=[y_axis[54],y_axis[54]]
ax.plot(line6_horizontal_start,line6_horizontal_end,color="gray",linestyle=':')

line7_vertical_start=[9,9]
line7_vertical_end=[0,y_axis[9]]
ax.plot(line7_vertical_start,line7_vertical_end,color="gray",linestyle=':')
line7_horizontal_start=[0,9]
line7_horizontal_end=[y_axis[9],y_axis[9]]
ax.plot(line7_horizontal_start,line7_horizontal_end,color="gray",linestyle=':')

line8_vertical_start=[60,60]
line8_vertical_end=[0,y_axis[60]]
ax.plot(line8_vertical_start,line8_vertical_end,color="gray",linestyle=':')
line8_horizontal_start=[0,60]
line8_horizontal_end=[y_axis[60],y_axis[60]]
ax.plot(line8_horizontal_start,line8_horizontal_end,color="gray",linestyle=':')

ax.plot(x_axis,y_axis,linestyle="",marker=".",color="b")

ax.set_xlim(xmin=-0.2)
ax.set_ylim(ymin=0)
plt.savefig('latency_graph_310_24hr_pcap.png',bbox_inches='tight')
plt.show()

# print("y_axis[18]: "+str(y_axis[18]))
# print("y_axis[27]: "+str(y_axis[27]))
# print("y_axis[36]: "+str(y_axis[36]))
# print("y_axis[45]: "+str(y_axis[45]))
# print("y_axis[53]: "+str(y_axis[53]))

# x = np.arange(0, math.pi*2, 0.05)
# fig = plt.figure()
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
# y = np.sin(x)
# ax.plot(x, y)
# plt.show()