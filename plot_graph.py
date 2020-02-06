import sys
import os
import decimal
import math
import matplotlib.pyplot as plt
import numpy as np
from hdrh.histogram import HdrHistogram
from hdrh.iterators import RecordedIterator

#-----Start-----Data generation-----Start-----

def value_range(start,stop,step):
    iteration_value=start
    loop_iterator=0
    while iteration_value < stop:
        yield iteration_value
        loop_iterator+=1
        iteration_value=decimal.Decimal(str(start))+(decimal.Decimal(str(step))*decimal.Decimal(str(loop_iterator)))

file_name = sys.argv[1] #name of the file containing latency numbers
sorted_data=[]
values_larger_than_9999_percentile=[]

file_name=file_name.split('.')
file_name=file_name[0]

# histogram __init__ values
LOWEST = 1
HIGHEST = 30000
SIGNIFICANT = 4

histogram = HdrHistogram(LOWEST, HIGHEST, SIGNIFICANT)

with open(file_name+'.txt','r') as in_file, open('sorted_'+file_name+'.txt','w') as out_file:
    for each_line in in_file:
        sorted_data.append(int(each_line))
    sorted_data.sort()
    for each_entry in sorted_data:
        out_file.write(str(each_entry)+'\n')
        histogram.record_value(each_entry)

histogram.output_percentile_distribution(open(file_name+'_histogram_file.csv', 'wb'), 1)
print("Histogram file (hdrm file) generated.\n")

#No need. Just open _graph_data.csv in w mode
if os.path.exists(file_name+'_graph_data.csv'):
    print('File '+file_name+'_graph_data.csv already exists. Removing ...')
    os.remove(file_name+'_graph_data.csv')
    print('File '+file_name+'_graph_data.csv removed.\n')

x_axis_location=0

with open(file_name+'_graph_data.csv','a') as graph_file:
    
    percentile_values=value_range(0,91,10)
    for percentile in percentile_values:
        graph_file.write(str(x_axis_location)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+',')
        graph_file.write(str(percentile)+'\n')
        x_axis_location+=1

    percentile_values=value_range(91,99,1)
    for percentile in percentile_values:
        graph_file.write(str(x_axis_location)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+',')
        graph_file.write(str(percentile)+'\n')
        x_axis_location+=1
    
    percentile_values=value_range(99,100,0.1)
    for percentile in percentile_values:
        graph_file.write(str(x_axis_location)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+',')
        graph_file.write(str(percentile)+'\n')
        x_axis_location+=1
    
    percentile_values=value_range(99.91,100,0.01)
    for percentile in percentile_values:
        graph_file.write(str(x_axis_location)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+',')
        graph_file.write(str(percentile)+'\n')
        x_axis_location+=1
    
    percentile_values=value_range(99.991,100,0.001)
    for percentile in percentile_values:
        graph_file.write(str(x_axis_location)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+',')
        graph_file.write(str(percentile)+'\n')
        x_axis_location+=1
    
    percentile_values=value_range(99.9991,100,0.0001)
    for percentile in percentile_values:
        graph_file.write(str(x_axis_location)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+',')
        graph_file.write(str(percentile)+'\n')
        x_axis_location+=1
    
    value_at_9999_percentile = histogram.get_value_at_percentile(99.9999)
    for each_entry in sorted_data:
        if each_entry > value_at_9999_percentile:
            values_larger_than_9999_percentile.append(each_entry)
    
    print("Values Larger than 9999: ")
    print(values_larger_than_9999_percentile)
    print("Total no of values larger than 9999 percentile: "+str(len(values_larger_than_9999_percentile))+"\n")
    count_of_values_larger_than_9999_percentile=0
    for each_entry in values_larger_than_9999_percentile:
        for item in histogram.get_recorded_iterator():
            #print("Value: "+str(item.value_iterated_to))
            #print(type(item.value_iterated_to))
            #print(type(each_entry))
            if item.value_iterated_to == each_entry:
                graph_file.write(str(x_axis_location)+',')
                graph_file.write(str(each_entry)+',')
                graph_file.write(str(item.percentile)+'\n')
                count_of_values_larger_than_9999_percentile+=1
                x_axis_location+=1

    if count_of_values_larger_than_9999_percentile!=len(values_larger_than_9999_percentile):
        print("Error: Not all values larger than 999 percentile plotted.")
        print("Solution: Increase value of SIGNIFICANT on line 22.")

print("graph_data (csv file) generated.\n")

#-----End-----Data generation-----End-----

#-----Start-----Plotting Graph using Matplotlib-----Start-----

x_axis=[]
y_axis=[]
graph_file=file_name+'_graph_data.csv'

with open(graph_file,'r') as in_file:
    for each_line in in_file:
        temp=each_line.split(',')
        x_axis.append(float(temp[0]))
        y_axis.append(float(temp[1]))

fig = plt.figure(figsize=(12, 8))
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

#---50th Percentile---
line1_vertical_start=[5,5]
line1_vertical_end=[0,y_axis[5]]
ax.plot(line1_vertical_start,line1_vertical_end,color="gray",linestyle=':')
line1_horizontal_start=[0,5]
line1_horizontal_end=[y_axis[5],y_axis[5]]
ax.plot(line1_horizontal_start,line1_horizontal_end,color="gray",linestyle=':')

#---90th Percentile---
line2_vertical_start=[9,9]
line2_vertical_end=[0,y_axis[9]]
ax.plot(line2_vertical_start,line2_vertical_end,color="gray",linestyle=':')
line2_horizontal_start=[0,9]
line2_horizontal_end=[y_axis[9],y_axis[9]]
ax.plot(line2_horizontal_start,line2_horizontal_end,color="gray",linestyle=':')

#---99th Percentile---
line3_vertical_start=[18,18]
line3_vertical_end=[0,y_axis[18]]
ax.plot(line3_vertical_start,line3_vertical_end,color="gray",linestyle=':')
line3_horizontal_start=[0,18]
line3_horizontal_end=[y_axis[18],y_axis[18]]
ax.plot(line3_horizontal_start,line3_horizontal_end,color="gray",linestyle=':')

#---99.9th Percentile---
line4_vertical_start=[27,27]
line4_vertical_end=[0,y_axis[27]]
ax.plot(line4_vertical_start,line4_vertical_end,color="gray",linestyle=':')
line4_horizontal_start=[0,27]
line4_horizontal_end=[y_axis[27],y_axis[27]]
ax.plot(line4_horizontal_start,line4_horizontal_end,color="gray",linestyle=':')

#---99.99th Percentile---
line5_vertical_start=[36,36]
line5_vertical_end=[0,y_axis[36]]
ax.plot(line5_vertical_start,line5_vertical_end,color="gray",linestyle=':')
line5_horizontal_start=[0,36]
line5_horizontal_end=[y_axis[36],y_axis[36]]
ax.plot(line5_horizontal_start,line5_horizontal_end,color="gray",linestyle=':')

#---99.999th Percentile---
line6_vertical_start=[45,45]
line6_vertical_end=[0,y_axis[45]]
ax.plot(line6_vertical_start,line6_vertical_end,color="gray",linestyle=':')
line6_horizontal_start=[0,45]
line6_horizontal_end=[y_axis[45],y_axis[45]]
ax.plot(line6_horizontal_start,line6_horizontal_end,color="gray",linestyle=':')

#---99.9999th Percentile---
line7_vertical_start=[54,54]
line7_vertical_end=[0,y_axis[54]]
ax.plot(line7_vertical_start,line7_vertical_end,color="gray",linestyle=':')
line7_horizontal_start=[0,54]
line7_horizontal_end=[y_axis[54],y_axis[54]]
ax.plot(line7_horizontal_start,line7_horizontal_end,color="gray",linestyle=':')

#---Max Value---
line8_vertical_start=[60,60]
line8_vertical_end=[0,y_axis[60]]
ax.plot(line8_vertical_start,line8_vertical_end,color="gray",linestyle=':')
line8_horizontal_start=[0,60]
line8_horizontal_end=[y_axis[60],y_axis[60]]
ax.plot(line8_horizontal_start,line8_horizontal_end,color="gray",linestyle=':')

ax.plot(x_axis,y_axis,linestyle="",marker=".",color="b")

ax.set_xlim(xmin=-0.2)
ax.set_ylim(ymin=0)

plt.savefig(file_name+'.png',bbox_inches='tight')
print("Graph plot saved in png file.\n")
print("Displaying graph.\n")
plt.show()

#-----End-----Plotting Graph using Matplotlib-----End-----