import sys
import os
import decimal
from hdrh.histogram import HdrHistogram
from hdrh.iterators import RecordedIterator


def value_range(start,stop,step):
    iteration_value=start
    loop_iterator=0
    while iteration_value < stop:
        yield iteration_value
        loop_iterator+=1
        iteration_value=decimal.Decimal(str(start))+(decimal.Decimal(str(step))*decimal.Decimal(str(loop_iterator)))


file_name = sys.argv[1]
sorted_data=[]
values_larger_than_999_percentile=[]

# histogram __init__ values
LOWEST = 1
HIGHEST = 30000
SIGNIFICANT = 4

histogram = HdrHistogram(LOWEST, HIGHEST, SIGNIFICANT)

with open(file_name,'r') as in_file, open('sorted_'+file_name,'w') as out_file:
    for each_line in in_file:
        sorted_data.append(int(each_line))
    sorted_data.sort()
    for each_entry in sorted_data:
        out_file.write(str(each_entry)+'\n')
        histogram.record_value(each_entry)

count = histogram.get_total_count()
value = histogram.get_value_at_percentile(99.9)
print("Value at percentile "+str(95)+": "+str(histogram.get_value_at_percentile(95)))

histogram.output_percentile_distribution(open('temp.csv', 'wb'), 1)
if os.path.exists('graph.csv'):
    os.remove('graph.csv')
    print('File removed')

with open('graph.csv','a') as graph_file:
    percentile_values=value_range(0,91,10)
    for percentile in percentile_values:
        graph_file.write(str(percentile)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+'\n')
    percentile_values=value_range(91,99,1)
    for percentile in percentile_values:
        graph_file.write(str(percentile)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+'\n')
    percentile_values=value_range(99,100,0.1)
    for percentile in percentile_values:
        graph_file.write(str(percentile)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+'\n')
    percentile_values=value_range(99.91,100,0.01)
    for percentile in percentile_values:
        graph_file.write(str(percentile)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+'\n')
    percentile_values=value_range(99.991,100,0.001)
    for percentile in percentile_values:
        graph_file.write(str(percentile)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+'\n')
    percentile_values=value_range(99.9991,100,0.0001)
    for percentile in percentile_values:
        graph_file.write(str(percentile)+',')
        graph_file.write(str(histogram.get_value_at_percentile(float(percentile)))+'\n')
    value_at_999_percentile = histogram.get_value_at_percentile(99.9999)
    for each_entry in sorted_data:
        if each_entry > value_at_999_percentile:
            values_larger_than_999_percentile.append(each_entry)
    
    print("Value Larger than 9999: ")
    print(values_larger_than_999_percentile)
    print(len(sorted_data))
    count_of_values_larger_than_999_percentile=0
    for each_entry in values_larger_than_999_percentile:
        for item in histogram.get_recorded_iterator():
            #print("Value: "+str(item.value_iterated_to))
            #print(type(item.value_iterated_to))
            #print(type(each_entry))
            if item.value_iterated_to == each_entry:
                graph_file.write(str(item.percentile)+',')
                graph_file.write(str(each_entry)+'\n')
                count_of_values_larger_than_999_percentile+=1
    if count_of_values_larger_than_999_percentile!=len(values_larger_than_999_percentile):
        print("Error: Not all values larger than 999 percentile plotted.")