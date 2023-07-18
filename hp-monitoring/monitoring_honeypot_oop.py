import psutil
import socket
import time
import netifaces as ni
import paho.mqtt.client as mqtt
import numpy as np
import uuid
import json
import os
from dotenv import load_dotenv
from datetime import datetime


class Monitoring:
    def __init__(self, processName):
        self.processName = processName

    def ipAddress():
        interfaces = ni.interfaces()
        for interface in interfaces:
            if 'wl' in interface: #dihapus line ini
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    ip_address = addresses[ni.AF_INET][0]['addr'] #ini pake template
        return (ip_address)

        # ip_address = '192.168.191.191'
        # return(ip_address)

    def ipGateway():
        gateways = ni.gateways()
        ip_gateway = ""
        
        if 'default' in gateways and ni.AF_INET in gateways['default']:
            for gw in gateways['default'][ni.AF_INET]:
                if gw[1] == 'wlan0':
                    ip_gateway = gw[0]
                    return ip_gateway
                    
        if ip_gateway:
            return ip_gateway
        else:
            interfaces = ni.interfaces()
            for interface in interfaces:
                if 'wl' in interface: #dihapus line ini
                    addresses = ni.ifaddresses(interface)
                    if ni.AF_INET in addresses:
                        ip_gateway = ni.gateways()['default'][ni.AF_INET][0]

            return (ip_gateway)

        # ip_gateway = '192.168.191.191'
        # return(ip_gateway)

    def checkHoneypotRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def checkProcessRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return(proc.status().capitalize())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def checkCPURunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return(proc.cpu_percent(interval=0.1))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return(proc.memory_percent())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def checkResidentMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return((proc.memory_info().rss) / 1024 / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkVirtualMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower()) or self.processName in proc.cmdline():
                    return((proc.memory_info().vms) / 1024 / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkTextMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return((proc.memory_info().text) / 1024 / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkDataMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return((proc.memory_info().data) / 1024 / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkSwapMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return((proc.memory_full_info().swap) / 1024 / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkRMSPercentRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return((proc.memory_percent(memtype='rss')))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkVMSPercentRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() or self.processName in proc.cmdline()):
                    return((proc.memory_percent(memtype='vms')))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
 
class Honeypot(Monitoring):

    # ==== TOTAL HONEYPOT RUNNING ====

    def totalHoneypotRunning():
        honeypot_total_running = np.array([Monitoring('dionaea').checkHoneypotRunning(), Monitoring('honeytrap').checkHoneypotRunning(), Monitoring('conpot').checkHoneypotRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkHoneypotRunning(), Monitoring('elasticpot.py').checkHoneypotRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkHoneypotRunning()])

        if True in honeypot_total_running:
            return(np.count_nonzero(honeypot_total_running == True))
        else:
            return(0)


    # ==== CHECK HONEYPOT STATUS ====

    def statusHoneypot():
        honeypot_process = [Monitoring('dionaea').checkProcessRunning(), Monitoring('honeytrap').checkProcessRunning(), Monitoring('conpot').checkProcessRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkProcessRunning(), Monitoring('elasticpot.py').checkProcessRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkProcessRunning()]
        status_honeypot_array = []
        for index in honeypot_process:
            if index == False:
                status_honeypot = 'Not Running'
            else:
                status_honeypot = index

            status_honeypot_array.append(status_honeypot)
        return(status_honeypot_array)
        
        
    # ==== CHECK HONEYPOT CPU ====

    def checkCPUHoneypot():
        honeypot_cpu = [Monitoring('dionaea').checkCPURunning(), Monitoring('honeytrap').checkCPURunning(), Monitoring('conpot').checkCPURunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkCPURunning(), Monitoring('elasticpot.py').checkCPURunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkCPURunning()]
        check_cpu_array = []
        for index in honeypot_cpu:
            if index == False:
                check_cpu = 0
            else:
                check_cpu = index

            check_cpu_array.append(check_cpu)
        return(check_cpu_array)
    

    # ==== CHECK HONEYPOT MEMORY PERCENT ====

    def checkMemoryHoneypot():
        honeypot_memory = [Monitoring('dionaea').checkMemoryRunning(), Monitoring('honeytrap').checkMemoryRunning(), Monitoring('conpot').checkMemoryRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkMemoryRunning(), Monitoring('elasticpot.py').checkMemoryRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkMemoryRunning()]
        check_memory_array = []
        for index in honeypot_memory:
            if index == False:
                check_memory = 0
            else:
                check_memory = index
                
            check_memory_array.append(check_memory)
        return(check_memory_array)
    

    # ==== CHECK HONEYPOT RMS ====

    def checkResidentMemoryHoneypot():
        honeypot_rms = [Monitoring('dionaea').checkResidentMemoryRunning(), Monitoring('honeytrap').checkResidentMemoryRunning(), Monitoring('conpot').checkResidentMemoryRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkResidentMemoryRunning(), Monitoring('elasticpot.py').checkResidentMemoryRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkResidentMemoryRunning()]
        check_rms_array = []
        for index in honeypot_rms:
            if index == False:
                check_rms = 0
            else:
                check_rms = index

            check_rms_array.append(check_rms)
        return(check_rms_array)


    # ==== CHECK HONEYPOT VMS ====

    def checkVirtualMemoryHoneypot():
        honeypot_vms = [Monitoring('dionaea').checkVirtualMemoryRunning(), Monitoring('honeytrap').checkVirtualMemoryRunning(), Monitoring('conpot').checkVirtualMemoryRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkVirtualMemoryRunning(), Monitoring('elasticpot.py').checkVirtualMemoryRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkVirtualMemoryRunning()]
        check_vms_array = []
        for index in honeypot_vms:
            if index == False:
                check_vms = 0
            else:
                check_vms = index

            check_vms_array.append(check_vms)
        return(check_vms_array)


    # ==== CHECK HONEYPOT TMS ====

    def checkTextMemoryHoneypot():
        honeypot_tms = [Monitoring('dionaea').checkTextMemoryRunning(), Monitoring('honeytrap').checkTextMemoryRunning(), Monitoring('conpot').checkTextMemoryRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkTextMemoryRunning(), Monitoring('elasticpot.py').checkTextMemoryRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkTextMemoryRunning()]
        check_tms_array = []
        for index in honeypot_tms:
            if index == False:
                check_tms = 0
            else:
                check_tms = index

            check_tms_array.append(check_tms)
        return(check_tms_array)


    # ==== CHECK HONEYPOT DATA MEMORY ====

    def checkDataMemoryHoneypot():
        honeypot_dms = [Monitoring('dionaea').checkDataMemoryRunning(), Monitoring('honeytrap').checkDataMemoryRunning(), Monitoring('conpot').checkDataMemoryRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkDataMemoryRunning(), Monitoring('elasticpot.py').checkDataMemoryRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkDataMemoryRunning()]
        check_dms_array = []
        for index in honeypot_dms:
            if index == False:
                check_dms = 0
            else:
                check_dms = index

            check_dms_array.append(check_dms)
        return(check_dms_array)
        

    # ==== CHECK HONEYPOT SHARED MEMORY ====

    def checkSwapMemoryHoneypot():
        honeypot_swap = [Monitoring('dionaea').checkSwapMemoryRunning(), Monitoring('honeytrap').checkSwapMemoryRunning(), Monitoring('conpot').checkSwapMemoryRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkSwapMemoryRunning(), Monitoring('elasticpot.py').checkSwapMemoryRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkSwapMemoryRunning()]
        check_swap_array = []
        for index in honeypot_swap:
            if index == False:
                check_swap = 0
            else:
                check_swap = index

            check_swap_array.append(check_swap)
        return(check_swap_array)


    # ==== CHECK HONEYPOT SWAP MEMORY ====

    def checkSwapMemoryHoneypot():
        honeypot_swap = [Monitoring('dionaea').checkSwapMemoryRunning(), Monitoring('honeytrap').checkSwapMemoryRunning(), Monitoring('conpot').checkSwapMemoryRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkSwapMemoryRunning(), Monitoring('elasticpot.py').checkSwapMemoryRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkSwapMemoryRunning()]
        check_swap_array = []
        for index in honeypot_swap:
            if index == False:
                check_swap = 0
            else:
                check_swap = index

            check_swap_array.append(check_swap)
        return(check_swap_array)  


    # ==== CHECK HONEYPOT RMS PERCENTAGE ====

    def checkRMSPercentHoneypot():
        honeypot_rms_percent = [Monitoring('dionaea').checkRMSPercentRunning(), Monitoring('honeytrap').checkRMSPercentRunning(), Monitoring('conpot').checkRMSPercentRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkRMSPercentRunning(), Monitoring('elasticpot.py').checkRMSPercentRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkRMSPercentRunning()]
        check_rms_percent_array = []
        for index in honeypot_rms_percent:
            if index == False:
                check_rms_percent = 0
            else:
                check_rms_percent = index

            check_rms_percent_array.append(check_rms_percent)
        return(check_rms_percent_array) 


    # ==== CHECK HONEYPOT VMS PERCENTAGE ====
     
    def checkVMSPercentHoneypot():
        honeypot_vms_percent = [Monitoring('dionaea').checkVMSPercentRunning(), Monitoring('honeytrap').checkVMSPercentRunning(), Monitoring('conpot').checkVMSPercentRunning(), Monitoring('/cowrie/cowrie-env/bin/python3').checkVMSPercentRunning(), Monitoring('elasticpot.py').checkVMSPercentRunning(), Monitoring('/rdpy/bin/rdpy-rdphoneypot.py').checkVMSPercentRunning()]
        check_vms_percent_array = []
        for index in honeypot_vms_percent:
            if index == False:
                check_vms_percent = 0
            else:
                check_vms_percent = index

            check_vms_percent_array.append(check_vms_percent)
        return(check_vms_percent_array)    


    # ==== RUNNING LOGS MONITORING HONEYPOT ====
    
    logs_json = None
    def main():
        global logs_json

        honeypot_state = Honeypot.statusHoneypot()
        honeypot_cpu = Honeypot.checkCPUHoneypot()
        honeypot_memory = Honeypot.checkMemoryHoneypot()
        honeypot_vms = Honeypot.checkVirtualMemoryHoneypot()
        honeypot_rms = Honeypot.checkResidentMemoryHoneypot()
        honeypot_tms = Honeypot.checkTextMemoryHoneypot()
        honeypot_dms = Honeypot.checkDataMemoryHoneypot()
        honeypot_swap = Honeypot.checkSwapMemoryHoneypot()
        honeypot_rms_percentage = Honeypot.checkRMSPercentHoneypot()
        honeypot_vms_percentage = Honeypot.checkVMSPercentHoneypot()

        logs_json = {
            "id_honeypot": str(uuid.uuid4()),
            "ip_address": Honeypot.ipAddress(),
            "ip_gateway": Honeypot.ipGateway(),
            "hostname": socket.gethostname(), #diganti template
            "honeypot_running": Honeypot.totalHoneypotRunning(),
            "dionaea_state": honeypot_state[0],
            "dionaea_cpu": float("{:.2f}".format(honeypot_cpu[0])),
            "dionaea_memory": float("{:.2f}".format(honeypot_memory[0])),
            "dionaea_virtual_memory": float("{:.2f}".format(honeypot_vms[0])),
            "dionaea_resident_memory": float("{:.2f}".format(honeypot_rms[0])),
            "dionaea_text_memory": float("{:.2f}".format(honeypot_tms[0])),
            "dionaea_data_memory": float("{:.2f}".format(honeypot_dms[0])),
            "dionaea_swap_memory": float("{:.2f}".format(honeypot_swap[0])),
            "dionaea_rms_percentage": float("{:.2f}".format(honeypot_rms_percentage[0])),
            "dionaea_vms_percentage": float("{:.2f}".format(honeypot_vms_percentage[0])),
            "honeytrap_state": honeypot_state[1],
            "honeytrap_cpu": float("{:.2f}".format(honeypot_cpu[1])),
            "honeytrap_memory": float("{:.2f}".format(honeypot_memory[1])),
            "honeytrap_virtual_memory": float("{:.2f}".format(honeypot_vms[1])),
            "honeytrap_resident_memory": float("{:.2f}".format(honeypot_rms[1])),
            "honeytrap_text_memory": float("{:.2f}".format(honeypot_tms[1])),
            "honeytrap_data_memory": float("{:.2f}".format(honeypot_dms[1])),
            "honeytrap_swap_memory": float("{:.2f}".format(honeypot_swap[1])),
            "honeytrap_rms_percentage": float("{:.2f}".format(honeypot_rms_percentage[1])),
            "honeytrap_vms_percentage": float("{:.2f}".format(honeypot_vms_percentage[1])),
            "gridpot_state": honeypot_state[2],
            "gridpot_cpu": float("{:.2f}".format(honeypot_cpu[2])),
            "gridpot_memory": float("{:.2f}".format(honeypot_memory[2])),
            "gridpot_virtual_memory": float("{:.2f}".format(honeypot_vms[2])),
            "gridpot_resident_memory": float("{:.2f}".format(honeypot_rms[2])),
            "gridpot_text_memory": float("{:.2f}".format(honeypot_tms[2])),
            "gridpot_data_memory": float("{:.2f}".format(honeypot_dms[2])),
            "gridpot_swap_memory": float("{:.2f}".format(honeypot_swap[2])),
            "gridpot_rms_percentage": float("{:.2f}".format(honeypot_rms_percentage[2])),
            "gridpot_vms_percentage": float("{:.2f}".format(honeypot_vms_percentage[2])),
            "cowrie_state": honeypot_state[3],
            "cowrie_cpu": float("{:.2f}".format(honeypot_cpu[3])),
            "cowrie_memory": float("{:.2f}".format(honeypot_memory[3])),
            "cowrie_virtual_memory": float("{:.2f}".format(honeypot_vms[3])),
            "cowrie_resident_memory": float("{:.2f}".format(honeypot_rms[3])),
            "cowrie_text_memory": float("{:.2f}".format(honeypot_tms[3])),
            "cowrie_data_memory": float("{:.2f}".format(honeypot_dms[3])),
            "cowrie_swap_memory": float("{:.2f}".format(honeypot_swap[3])),
            "cowrie_rms_percentage": float("{:.2f}".format(honeypot_rms_percentage[3])),
            "cowrie_vms_percentage": float("{:.2f}".format(honeypot_vms_percentage[3])),
            "elasticpot_state": honeypot_state[4],
            "elasticpot_cpu": float("{:.2f}".format(honeypot_cpu[4])),
            "elasticpot_memory": float("{:.2f}".format(honeypot_memory[4])),
            "elasticpot_virtual_memory": float("{:.2f}".format(honeypot_vms[4])),
            "elasticpot_resident_memory": float("{:.2f}".format(honeypot_rms[4])),
            "elasticpot_text_memory": float("{:.2f}".format(honeypot_tms[4])),
            "elasticpot_data_memory": float("{:.2f}".format(honeypot_dms[4])),
            "elasticpot_swap_memory": float("{:.2f}".format(honeypot_swap[4])),
            "elasticpot_rms_percentage": float("{:.2f}".format(honeypot_rms_percentage[4])),
            "elasticpot_vms_percentage": float("{:.2f}".format(honeypot_vms_percentage[4])),
            "rdpy_state": honeypot_state[5],
            "rdpy_cpu": float("{:.2f}".format(honeypot_cpu[5])),
            "rdpy_memory": float("{:.2f}".format(honeypot_memory[5])),
            "rdpy_virtual_memory": float("{:.2f}".format(honeypot_vms[5])),
            "rdpy_resident_memory": float("{:.2f}".format(honeypot_rms[5])),
            "rdpy_text_memory": float("{:.2f}".format(honeypot_tms[5])),
            "rdpy_data_memory": float("{:.2f}".format(honeypot_dms[5])),
            "rdpy_swap_memory": float("{:.2f}".format(honeypot_swap[5])),
            "rdpy_rms_percentage": float("{:.2f}".format(honeypot_rms_percentage[5])),
            "rdpy_vms_percentage": float("{:.2f}".format(honeypot_vms_percentage[5])),
            "datetime": datetime.now().isoformat()
        }

        return logs_json

class MQTT(Honeypot):

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
            result = client.publish(os.getenv('MQTT_TOPIC_HONEYPOT'), msg, qos=1, retain=True)
            status = result[0]
            if status == 0:
                print(msg)
            else:
                print(f"Failed to send message to topic {os.getenv('MQTT_TOPIC_HONEYPOT')}")
        except:
            print("Failed to parse data")

    # ==== RUN MQTT ====

    def run():
        Honeypot.main()
        MQTT.publish(client)

if __name__ == '__main__':
    client = MQTT.connect_mqtt()
    client.loop_start()

    MQTT.run()
 