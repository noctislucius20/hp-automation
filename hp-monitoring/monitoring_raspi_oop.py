import psutil
import socket
import netifaces as ni
import paho.mqtt.client as mqtt
import json
import numpy as np
import uuid
import os
from dotenv import load_dotenv
from datetime import datetime


class Monitoring:
    def __init__(self, processName, status):
        self.processName = processName
        self.status = status
    
    #Fungsi Penggunaan Persentase CPU
    def cpu_usage():
        return psutil.cpu_percent(interval=0.5)

    #Fungsi Frekuensi CPU
    def cpu_frequency():
        return psutil.cpu_freq().current

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

    # Fungsi Network I/O Paket yang diterima
    def network_packet_recv():
        return psutil.net_io_counters().packets_recv   

    # Fungsi Network I/O Paket yang terkirim 
    def network_packet_sent():
        return psutil.net_io_counters().packets_sent
    
    def checkHoneypotRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def ipAddress():
        ipAddress = []
        interfaces = ni.interfaces()
        
        for interface in interfaces:
            if 'eth' in interface or 'en' in interface or 'wlan' in interface:
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    ipAddress.append(interface)
                    ipAddress.append(addresses[ni.AF_INET][0]['addr'])

        return ipAddress

class Raspi(Monitoring):
    def totalHoneypotRunning():
        dionaea_running = Monitoring('dionaea', 'running').checkHoneypotRunning()
        dionaea_sleeping = Monitoring('dionaea', 'sleeping').checkHoneypotRunning()
        honeytrap_running = Monitoring('honeytrap', 'running').checkHoneypotRunning()
        honeytrap_sleeping = Monitoring('honeytrap', 'sleeping').checkHoneypotRunning()
        gridpot_running = Monitoring('conpot', 'running').checkHoneypotRunning()
        gridpot_sleeping = Monitoring('conpot', 'sleeping').checkHoneypotRunning()
        cowrie_running = Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkHoneypotRunning()
        cowrie_sleeping = Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkHoneypotRunning()
        elasticpot_running = Monitoring('elasticpot.py', 'running').checkHoneypotRunning()
        elasticpot_sleeping = Monitoring('elasticpot.py', 'sleeping').checkHoneypotRunning()
        rdpy_running = Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkHoneypotRunning()
        rdpy_sleeping = Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkHoneypotRunning()

        list_honeypot_running = np.array([dionaea_running, honeytrap_running, gridpot_running, cowrie_running, elasticpot_running, rdpy_running])
        list_honeypot_sleeping = np.array([dionaea_sleeping, honeytrap_sleeping, gridpot_sleeping, cowrie_sleeping, elasticpot_sleeping, rdpy_sleeping])

        if True in list_honeypot_running:
            return(np.count_nonzero(list_honeypot_running == True))
        elif True in list_honeypot_sleeping:
            return(np.count_nonzero(list_honeypot_sleeping == True))
        else:
            return(0)
        
    def main():
        global logs_json
        logs_json = {
            "id_raspi": str(uuid.uuid4()),
            "ip_address": Monitoring.ipAddress(),
            "hostname": socket.gethostname(),
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
        client.connect(os.getenv('MQTT_BROKER_2'), int(os.getenv('MQTT_PORT')))
        return client

    # ==== START MQTT PUBLISH ====

    def publish(client):
        try:
                
            msg = json.dumps(logs_json)
            result = client.publish(os.getenv('MQTT_TOPIC_SENSOR'), msg, qos=2)
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