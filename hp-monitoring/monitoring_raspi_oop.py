import psutil
import socket
import time
import netifaces as ni
import paho.mqtt.client as mqtt
import json
import numpy as np
import uuid
import os
import docker
from dotenv import load_dotenv
from datetime import datetime


class Monitoring:
    def __init__(self, processName):
        self.processName = processName
    
    #Fungsi Penggunaan Persentase CPU
    def cpu_usage():
        return psutil.cpu_percent(interval=0.1)

    #Fungsi Frekuensi CPU
    def cpu_frequency():
        return psutil.cpu_freq().current

    #Fungsi Total CPU
    def cpu_count():
        return psutil.cpu_count()

    #Fungsi Total RAM dalam bentuk MB (Virtual Memory)
    def ram_total():
        return (psutil.virtual_memory().total) / (1024 * 1024)

    #Fungsi Penggunaan RAM dalam bentuk MB (Virtual Memory)
    def ram_usage():
        return (psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024 * 1024)

    #Fungsi Tersediaan RAM dalam bentuk MB (Virtual Memory)
    def ram_available():
        return (psutil.virtual_memory().available) / (1024 * 1024)   

    #Fungsi Persentase Penggunaan RAM
    def ram_percent():
        return psutil.virtual_memory().percent     

    #Fungsi Total Swap Memory dalam Bentuk MB
    def swap_memory_total():
        return (psutil.swap_memory().total) / (1024 * 1024)

    #Fungsi Penggunaan Swap Memory dalam Bentuk MB
    def swap_memory_usage():
        return (psutil.swap_memory().used) / (1024 * 1024)

    #Fungsi Tersediaan Swap Memory dalam Bentuk MB
    def swap_memory_free():
        return (psutil.swap_memory().free) / (1024 * 1024)

    #Fungsi Persentase Penggunaan Swap Memory dalam Bentuk MB
    def swap_memory_percentage():
        return psutil.swap_memory().percent

    # Fungsi Network I/O Paket yang diterima
    def network_packet_recv():
        return psutil.net_io_counters().packets_recv   

    # Fungsi Network I/O Paket yang terkirim 
    def network_packet_sent():
        return psutil.net_io_counters().packets_sent
    
    def checkHoneypotRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkStorage():
        usage = psutil.disk_usage('/')
        storage_array = []

        total_storage = usage.total / (1024**3)
        used_storage = usage.used / (1024**3)
        free_storage = usage.free / (1024**3)

        storage_array.append(total_storage)
        storage_array.append(used_storage)
        storage_array.append(free_storage)

        return (storage_array)

    def ipAddress():
        # interfaces = ni.interfaces()
        # for interface in interfaces:
        #     if 'wl' in interface: #dihapus line ini
        #         addresses = ni.ifaddresses(interface)
        #         if ni.AF_INET in addresses:
        #             ip_address = addresses[ni.AF_INET][0]['addr'] #ini pake template
        #             # ip_gateway = gateways['default'][ni.AF_INET][0]
        # return (ip_address)

        ip_address = '192.168.191.191'
        return(ip_address)

    def ipGateway():
        # gateways = ni.gateways()
        # ip_gateway = ""
        
        # if 'default' in gateways and ni.AF_INET in gateways['default']:
        #     for gw in gateways['default'][ni.AF_INET]:
        #         if gw[1] == 'wl':
        #             ip_gateway = gw[0]
        #             return ip_gateway
                    
        # if ip_gateway:
        #     return ip_gateway
        # else:
        #     interfaces = ni.interfaces()
        #     for interface in interfaces:
        #         if 'wl' in interface: #dihapus line ini
        #             addresses = ni.ifaddresses(interface)
        #             if ni.AF_INET in addresses:
        #                 ip_gateway = ni.gateways()['default'][ni.AF_INET][0] #ini pake template

        #     return (ip_gateway)

        ip_gateway = '192.168.191.191'
        return(ip_gateway)

class Raspi(Monitoring):
    def totalHoneypotRunning():
        honeypot_total_running = np.array([Monitoring('dionaea').checkHoneypotRunning(), Monitoring('honeytrap').checkHoneypotRunning(), Monitoring('conpot').checkHoneypotRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkHoneypotRunning(), Monitoring('elasticpot.py').checkHoneypotRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkHoneypotRunning()])

        if True in honeypot_total_running:
            return(np.count_nonzero(honeypot_total_running == True))
        else:
            return(0)
        
    def main():
        raspi_storage = Monitoring.checkStorage()

        global logs_json
        logs_json = {
            "id_raspi": str(uuid.uuid4()),
            "ip_address": Monitoring.ipAddress(),
            "ip_gateway": Monitoring.ipGateway(),
            "hostname": socket.gethostname(), #ini ganti template
            "honeypot_running": Raspi.totalHoneypotRunning(),
            "CPU_usage": Monitoring.cpu_usage(),
            "CPU_frequency": float("{:.2f}".format(Monitoring.cpu_frequency())),
            "CPU_count": Monitoring.cpu_count(),
            "RAM_total": float("{:.2f}".format(Monitoring.ram_total())),
            "RAM_usage": float("{:.2f}".format(Monitoring.ram_usage())),
            "RAM_available": float("{:.2f}".format(Monitoring.ram_available())),
            "RAM_percentage": Monitoring.ram_percent(),
            "swap_memory_total": float("{:.2f}".format(Monitoring.swap_memory_total())),
            "swap_memory_usage": float("{:.2f}".format(Monitoring.swap_memory_usage())),
            "swap_memory_free": float("{:.2f}".format(Monitoring.swap_memory_free())),
            "swap_memory_percentage": Monitoring.swap_memory_percentage(),
            "storage_total": float("{:.2f}".format(raspi_storage[0])),
            "storage_used": float("{:.2f}".format(raspi_storage[1])),
            "storage_free": float("{:.2f}".format(raspi_storage[2])),
            "network_packet_recv": Monitoring.network_packet_recv(),
            "network_packet_sent": Monitoring.network_packet_sent(),
            "datetime": datetime.now().isoformat()
            }
        
        return logs_json

class MQTT(Raspi):

    # ==== START MQTT CONNECTION ====

    load_dotenv()

    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt.Client(os.getenv('MQTT_CLIENT_HONEYPOT'))
        client.on_connect = on_connect
        client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')))
        return client

    # ==== START MQTT PUBLISH ====

    def publish(client):
        try:  
            msg = json.dumps(logs_json)
            result = client.publish(os.getenv('MQTT_TOPIC_SENSOR'), msg, qos=1, retain=True)
            status = result[0]
            if status == 0:
                print(msg)
            else:
                print(f"Failed to send message to topic {os.getenv('MQTT_TOPIC_SENSOR')}")
        except:
            print("Failed to parse data")

    # ==== RUN MQTT ====

    def run():
        Raspi.main()
        MQTT.publish(client)

if __name__ == '__main__':
    client = MQTT.connect_mqtt()
    client.loop_start()
    
    MQTT.run()