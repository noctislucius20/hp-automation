import psutil
import os
import time
import json
import schedule
import humanize

#Fungsi Penggunaan Setiap CPU
# def cpu_usage_percpu():
#     return psutil.cpu_percent(interval=0.5, percpu=True)

#Fungsi Penggunaan Persentase CPU
def cpu_usage():
    return psutil.cpu_percent(interval=0.5)

#Fungsi Frekuensi CPU
def cpu_frequency():
    return psutil.cpu_freq().current

#Fungsi Temperatur CPU
# def cpu_temperature():
#     result = 0.0
#     if  os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
#         with open('/sys/class/thermal/thermal_zone0/temp') as f:
#             line = f.readline().strip()
#         if line.isdigit():
#             result = float(line) / 1000
#     return result

#Fungsi Total CPU
def cpu_count():
    return psutil.cpu_count()

#Fungsi Total RAM dalam bentuk MB (Virtual Memory)
def ram_total():
    return (psutil.virtual_memory().total) / 1024 / 1024

#Fungsi Penggunaan RAM dalam bentuk MB (Virtual Memory)
def ram_usage():
    return (psutil.virtual_memory().total - psutil.virtual_memory().available) / 1024 / 1024

#Fungsi Tersediaan RAM dalam bentuk MB (Virtual Memory)
def ram_available():
    return (psutil.virtual_memory().available) / 1024 / 1024   

#Fungsi Persentase Penggunaan RAM
def ram_percent():
    return psutil.virtual_memory().percent     

#Fungsi Total Swap Memory dalam Bentuk MB
def swap_memory_total():
    return (psutil.swap_memory().total) / 1024 / 1024

#Fungsi Penggunaan Swap Memory dalam Bentuk MB
def swap_memory_usage():
    return (psutil.swap_memory().used) / 1024 / 1024

#Fungsi Tersediaan Swap Memory dalam Bentuk MB
def swap_memory_free():
    return (psutil.swap_memory().free) / 1024 / 1024

#Fungsi Persentase Penggunaan Swap Memory dalam Bentuk MB
def swap_memory_percentage():
    return psutil.swap_memory().percent

#Fungsi Penggunaan Disk Space Total
# def disk_space_total():
#     return psutil.disk_usage('/').total

# Fungsi Network I/O Paket yang diterima
def network_packet_recv():
    return psutil.net_io_counters().packets_recv   

# Fungsi Network I/O Paket yang terkirim 
def network_packet_sent():
    return psutil.net_io_counters().packets_sent   

def home():
#    cpu_usage_cpu = cpu_usage_percpu()
    cpu_use = cpu_usage()
    cpu_freq = float("{:.2f}".format(cpu_frequency()))
    # cpu_temp = float(cpu_temperature())
    cpu_cnt = cpu_count()
    ram_tot = float("{:.2f}".format(ram_total()))
    ram_use = float("{:.2f}".format(ram_usage()))
    ram_avail = float("{:.2f}".format(ram_available()))
    ram_percentage = ram_percent()
    swap_tot = float("{:.2f}".format(swap_memory_total()))
    swap_use = float("{:.2f}".format(swap_memory_usage()))
    swap_free = float("{:.2f}".format(swap_memory_free()))
    swap_percentage = swap_memory_percentage()
    # disk_tot = disk_space_total()
    network_pkt_recv = network_packet_recv()
    network_pkt_sent = network_packet_sent()

    logs_json = {
#        "CPU_usage_percpu": cpu_usage_cpu,
        "CPU_usage": cpu_use,
        "CPU_frequency": cpu_freq,
        # "CPU_temperature": cpu_temp,
        "CPU_count": cpu_cnt,
        "RAM_total": ram_tot,
        "RAM_usage": ram_use,
        "RAM_available": ram_avail,
        "RAM_percentage": ram_percentage,
        "swap_memory_total": swap_tot,
        "swap_memory_usage": swap_use,
        "swap_memory_free": swap_free,
        "swap_memory_percentage": swap_percentage,
        # "disk_total": disk_tot,
        "network_packet_recv": network_pkt_recv,
        "network_packet_sent": network_pkt_sent
        }
    
    with open('logs.json', 'a+') as json_file:
        json.dump(logs_json, json_file)
        json_file.write("\n")

    # print(logs_json)

schedule.every(30).seconds.do(home)

while True:
    schedule.run_pending()
    time.sleep(1)