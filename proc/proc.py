import os
import time

def get_cpu_infor():
    pre_data = {}
    while True:
        data = {}
        try:
            for line in open('/proc/stat', 'r', encoding = 'utf-8'):
                if 'cpu' in line:
                    line = line.replace('\n', '').replace('  ', ' ').split(' ')
                    key = line[0]
                    values = [int(value) for value in line[1:]]
                    cpu_time = sum(values)
                    idle = values[3]
                    data[key] = [cpu_time,idle]
        except:
            yield {}
            continue
        result = { }
        if pre_data == { }:
            for key in data:
                result[key] = 0
        else:
            for key in data:
                total_cpu_time = data[key][0] - pre_data[key][0]
                idle_cpu_time = data[key][1] - pre_data[key][1]
                result[key] = (total_cpu_time - idle_cpu_time) / total_cpu_time
        yield result
        pre_data = data


def get_memory_infor():
    result = {}
    try:
        for line in open('/proc/meminfo', 'r', encoding = 'utf-8'):
            line = line.replace('\n', '').replace('\t', '').replace(' ', '').split(':')
            key = line[0]
            value = int(line[1].replace('kB', ''))/1024
            result[key] = value
    except:
        return {}
    return result


def get_network_infor():
    pre_data = { }
    while True:
        data = { }
        try:
            for line in open('/proc/net/dev', 'r', encoding = 'utf-8'):
                if '|' in line:
                    continue
                result_line = ''
                line = line.replace('\n', '').replace('\t', '')
                for i in range(len(line)):
                    if i != 0 and line[i] == line[i - 1] and line[i] == ' ':
                        continue
                    result_line += line[i]
                key =line.split(':')[0].replace(' ', '')
                values = [int(value) for value in line.split(':')[1].split(' ') if value != '']
                data[key] = [values[0],values[8]]
        except:
            yield {}
            continue
        result = { }
        if pre_data == { }:
            for key in data:
                result[key] = data[key]
                result[key] += [0,0]
        else:
            for key in data:
                try:
                    down_speed = data[key][0] - pre_data[key][0]
                    up_speed = data[key][1] - pre_data[key][1]
                except:
                    down_speed = 0
                    up_speed = 0
                result[key] = data[key]
                result[key] += [down_speed/1024,up_speed/1024]
        yield result
        pre_data = data

def get_process_infor():
    result = []
    for dirname in os.listdir('/proc'):
        try:
            pid = int(dirname)
        except:
            continue
        item={}
        for line in open('/proc/%s/status'%dirname,'r',encoding='utf-8'):
            line = line.replace('\n', '').replace('\t', '').replace(' ', '').split(':')
            key = line[0]
            value = line[1]
            item[key] = value
        result.append(item)
    return result
