import psutil
import socket
import netifaces as ni
import paho.mqtt.client as mqtt
import numpy as np
import uuid
import json
import os
from dotenv import load_dotenv
from datetime import datetime


class Monitoring:
    def __init__(self, processName, status):
        self.processName = processName
        self.status = status

    def ipAddress():
        ipAddress = []
        interfaces = ni.interfaces()
        
        for interface in interfaces:
            if 'eth' in interface or 'en' in interface:
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    ipAddress.append(interface)
                    ipAddress.append(addresses[ni.AF_INET][0]['addr'])

        return ipAddress

    def checkHoneypotRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def checkIfProcessRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return(proc.status().capitalize())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def checkCPURunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return(proc.cpu_percent())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def checkResidentMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return((proc.memory_info().rss) / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkVirtualMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower()) or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower():
                    return((proc.memory_info().vms) / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkTextMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return((proc.memory_info().text) / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkDataMemoryRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return((proc.memory_info().data) / 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkRMSPercentRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return((proc.memory_percent(memtype='rss')))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def checkVMSPercentRunning(self):
        for proc in psutil.process_iter():
            try:
                if (self.processName.lower() in proc.name().lower() and self.status.lower() in proc.status().lower() or self.processName in proc.cmdline() and self.status.lower() in proc.status().lower()):
                    return((proc.memory_percent(memtype='vms')))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
 
class Honeypot(Monitoring):

    # ==== TOTAL HONEYPOT RUNNING ====

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


    # ==== CHECK HONEYPOT STATUS ====
        
    def checkDionaea():
        if Monitoring('dionaea', 'running').checkIfProcessRunning():
            return(Monitoring('dionaea', 'running').checkIfProcessRunning())
        elif Monitoring('dionaea', 'sleeping').checkIfProcessRunning():
            return(Monitoring('dionaea', 'sleeping').checkIfProcessRunning())
        else:
            return('Not Running')
    
    def checkHoneytrap():
        if Monitoring('honeytrap', 'running').checkIfProcessRunning():
            return Monitoring('honeytrap', 'running').checkIfProcessRunning()
        elif Monitoring('honeytrap', 'sleeping').checkIfProcessRunning():
            return Monitoring('honeytrap', 'sleeping').checkIfProcessRunning()
        else:
            return('Not Running')
        
    def checkGridpot():
        if Monitoring('conpot', 'running').checkIfProcessRunning():
            return Monitoring('conpot', 'running').checkIfProcessRunning()
        elif Monitoring('conpot', 'sleeping').checkIfProcessRunning():
            return Monitoring('conpot', 'sleeping').checkIfProcessRunning()
        else:
            return('Not Running')

    def checkCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkIfProcessRunning():
            return (Monitoring('/cowrie/cowrie-env/bin/python3', 'running')).checkIfProcessRunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkIfProcessRunning():
            return (Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping')).checkIfProcessRunning()
        else:
            return('Not Running')

    def checkElasticpot():
        if Monitoring('elasticpot.py', 'running').checkIfProcessRunning():
            return (Monitoring('elasticpot.py', 'running')).checkIfProcessRunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkIfProcessRunning():
            return (Monitoring('elasticpot.py', 'sleeping')).checkIfProcessRunning()
        else:
            return('Not Running')

    def checkRDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkIfProcessRunning():
            return (Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running')).checkIfProcessRunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkIfProcessRunning():
            return (Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')).checkIfProcessRunning()
        else:
            return('Not Running')
        
        
    # ==== CHECK HONEYPOT CPU ====

    def checkCPUDionaea():
        if Monitoring('dionaea', 'running').checkCPURunning():
            return Monitoring('dionaea', 'running').checkCPURunning()
        elif Monitoring('dionaea', 'sleeping').checkCPURunning():
            return Monitoring('dionaea', 'sleeping').checkCPURunning()
        else:
            return(0)

    def checkCPUHoneytrap():
        if Monitoring('honeytrap', 'running').checkCPURunning():
            return Monitoring('honeytrap', 'running').checkCPURunning()
        elif Monitoring('honeytrap', 'sleeping').checkCPURunning():
            return Monitoring('honeytrap', 'sleeping').checkCPURunning()
        else:
            return(0)

    def checkCPUGridpot():
        if Monitoring('conpot', 'running').checkCPURunning():
            return Monitoring('conpot', 'running').checkCPURunning()
        elif Monitoring('conpot', 'sleeping').checkCPURunning():
            return Monitoring('conpot', 'sleeping').checkCPURunning()
        else:
            return(0)

    def checkCPUCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkCPURunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkCPURunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkCPURunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkCPURunning()
        else:
            return(0)

    def checkCPUElasticpot():
        if Monitoring('elasticpot.py', 'running').checkCPURunning():
            return Monitoring('elasticpot.py', 'running').checkCPURunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkCPURunning():
            return Monitoring('elasticpot.py', 'sleeping').checkCPURunning()
        else:
            return(0)

    def checkCPURDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkCPURunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkCPURunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkCPURunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkCPURunning()
        else:
            return(0)

    # ==== CHECK HONEYPOT RMS ====

    def checkResidentMemoryDionaea():
        if Monitoring('dionaea', 'running').checkResidentMemoryRunning():
            return Monitoring('dionaea', 'running').checkResidentMemoryRunning()
        elif Monitoring('dionaea', 'sleeping').checkResidentMemoryRunning():
            return Monitoring('dionaea', 'sleeping').checkResidentMemoryRunning()
        else:
            return(0)

    def checkResidentMemoryHoneytrap():
        if Monitoring('honeytrap', 'running').checkResidentMemoryRunning():
            return Monitoring('honeytrap', 'running').checkResidentMemoryRunning()
        elif Monitoring('honeytrap', 'sleeping').checkResidentMemoryRunning():
            return Monitoring('honeytrap', 'sleeping').checkResidentMemoryRunning()
        else:
            return(0)

    def checkResidentMemoryGridpot():
        if Monitoring('conpot', 'running').checkResidentMemoryRunning():
            return Monitoring('conpot', 'running').checkResidentMemoryRunning()
        elif Monitoring('conpot', 'sleeping').checkResidentMemoryRunning():
            return Monitoring('conpot', 'sleeping').checkResidentMemoryRunning()
        else:
            return(0)

    def checkResidentMemoryCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkResidentMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkResidentMemoryRunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkResidentMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkResidentMemoryRunning()
        else:
            return(0)

    def checkResidentMemoryElasticpot():
        if Monitoring('elasticpot.py', 'running').checkResidentMemoryRunning():
            return Monitoring('elasticpot.py', 'running').checkResidentMemoryRunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkResidentMemoryRunning():
            return Monitoring('elasticpot.py', 'sleeping').checkResidentMemoryRunning()
        else:
            return(0)

    def checkResidentMemoryRDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkResidentMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkResidentMemoryRunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkResidentMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkResidentMemoryRunning()
        else:
            return(0)


    # ==== CHECK HONEYPOT VMS ====

    def checkVirtualMemoryDionaea():
        if Monitoring('dionaea', 'running').checkVirtualMemoryRunning():
            return Monitoring('dionaea', 'running').checkVirtualMemoryRunning()
        elif Monitoring('dionaea', 'sleeping').checkVirtualMemoryRunning():
            return Monitoring('dionaea', 'sleeping').checkVirtualMemoryRunning()
        else:
            return(0)

    def checkVirtualMemoryHoneytrap():
        if Monitoring('honeytrap', 'running').checkVirtualMemoryRunning():
            return Monitoring('honeytrap', 'running').checkVirtualMemoryRunning()
        elif Monitoring('honeytrap', 'sleeping').checkVirtualMemoryRunning():
            return Monitoring('honeytrap', 'sleeping').checkVirtualMemoryRunning()
        else:
            return(0)

    def checkVirtualMemoryGridpot():
        if Monitoring('conpot', 'running').checkVirtualMemoryRunning():
            return Monitoring('conpot', 'running').checkVirtualMemoryRunning()
        elif Monitoring('conpot', 'sleeping').checkVirtualMemoryRunning():
            return Monitoring('conpot', 'sleeping').checkVirtualMemoryRunning()
        else:
            return(0)

    def checkVirtualMemoryCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkVirtualMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkVirtualMemoryRunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkVirtualMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkVirtualMemoryRunning()
        else:
            return(0)

    def checkVirtualMemoryElasticpot():
        if Monitoring('elasticpot.py', 'running').checkVirtualMemoryRunning():
            return Monitoring('elasticpot.py', 'running').checkVirtualMemoryRunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkVirtualMemoryRunning():
            return Monitoring('elasticpot.py', 'sleeping').checkVirtualMemoryRunning()
        else:
            return(0)

    def checkVirtualMemoryRDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkVirtualMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkVirtualMemoryRunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkVirtualMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkVirtualMemoryRunning()
        else:
            return(0)


    # ==== CHECK HONEYPOT TMS ====

    def checkTextMemoryDionaea():
        if Monitoring('dionaea', 'running').checkTextMemoryRunning():
            return Monitoring('dionaea', 'running').checkTextMemoryRunning()
        elif Monitoring('dionaea', 'sleeping').checkTextMemoryRunning():
            return Monitoring('dionaea', 'sleeping').checkTextMemoryRunning()
        else:
            return(0)

    def checkTextMemoryHoneytrap():
        if Monitoring('honeytrap', 'running').checkTextMemoryRunning():
            return Monitoring('honeytrap', 'running').checkTextMemoryRunning()
        elif Monitoring('honeytrap', 'sleeping').checkTextMemoryRunning():
            return Monitoring('honeytrap', 'sleeping').checkTextMemoryRunning()
        else:
            return(0)

    def checkTextMemoryGridpot():
        if Monitoring('conpot', 'running').checkTextMemoryRunning():
            return Monitoring('conpot', 'running').checkTextMemoryRunning()
        elif Monitoring('conpot', 'sleeping').checkTextMemoryRunning():
            return Monitoring('conpot', 'sleeping').checkTextMemoryRunning()
        else:
            return(0)

    def checkTextMemoryCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkTextMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkTextMemoryRunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkTextMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkTextMemoryRunning()
        else:
            return(0)

    def checkTextMemoryElasticpot():
        if Monitoring('elasticpot.py', 'running').checkTextMemoryRunning():
            return Monitoring('elasticpot.py', 'running').checkTextMemoryRunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkTextMemoryRunning():
            return Monitoring('elasticpot.py', 'sleeping').checkTextMemoryRunning()
        else:
            return(0)

    def checkTextMemoryRDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkTextMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkTextMemoryRunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkTextMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkTextMemoryRunning()
        else:
            return(0)


    # ==== CHECK HONEYPOT DATA MEMORY ====
        
    def checkDataMemoryDionaea():
        if Monitoring('dionaea', 'running').checkDataMemoryRunning():
            return Monitoring('dionaea', 'running').checkDataMemoryRunning()
        elif Monitoring('dionaea', 'sleeping').checkDataMemoryRunning():
            return Monitoring('dionaea', 'sleeping').checkDataMemoryRunning()
        else:
            return(0)

    def checkDataMemoryHoneytrap():
        if Monitoring('honeytrap', 'running').checkDataMemoryRunning():
            return Monitoring('honeytrap', 'running').checkDataMemoryRunning()
        elif Monitoring('honeytrap', 'sleeping').checkDataMemoryRunning():
            return Monitoring('honeytrap', 'sleeping').checkDataMemoryRunning()
        else:
            return(0)

    def checkDataMemoryGridpot():
        if Monitoring('conpot', 'running').checkDataMemoryRunning():
            return Monitoring('conpot', 'running').checkDataMemoryRunning()
        elif Monitoring('conpot', 'sleeping').checkDataMemoryRunning():
            return Monitoring('conpot', 'sleeping').checkDataMemoryRunning()
        else:
            return(0)

    def checkDataMemoryCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkDataMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkDataMemoryRunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkDataMemoryRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkDataMemoryRunning()
        else:
            return(0)

    def checkDataMemoryElasticpot():
        if Monitoring('elasticpot.py', 'running').checkDataMemoryRunning():
            return Monitoring('elasticpot.py', 'running').checkDataMemoryRunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkDataMemoryRunning():
            return Monitoring('elasticpot.py', 'sleeping').checkDataMemoryRunning()
        else:
            return(0)

    def checkDataMemoryRDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkDataMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkDataMemoryRunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkDataMemoryRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkDataMemoryRunning()
        else:
            return(0)


    # ==== CHECK HONEYPOT RMS PERCENTAGE ==== 
        
    def checkRMSPercentDionaea():
        if Monitoring('dionaea', 'running').checkRMSPercentRunning():
            return Monitoring('dionaea', 'running').checkRMSPercentRunning()
        elif Monitoring('dionaea', 'sleeping').checkRMSPercentRunning():
            return Monitoring('dionaea', 'sleeping').checkRMSPercentRunning()
        else:
            return(0)

    def checkRMSPercentHoneytrap():
        if Monitoring('honeytrap', 'running').checkRMSPercentRunning():
            return Monitoring('honeytrap', 'running').checkRMSPercentRunning()
        elif Monitoring('honeytrap', 'sleeping').checkRMSPercentRunning():
            return Monitoring('honeytrap', 'sleeping').checkRMSPercentRunning()
        else:
            return(0)

    def checkRMSPercentGridpot():
        if Monitoring('conpot', 'running').checkRMSPercentRunning():
            return Monitoring('conpot', 'running').checkRMSPercentRunning()
        elif Monitoring('conpot', 'sleeping').checkRMSPercentRunning():
            return Monitoring('conpot', 'sleeping').checkRMSPercentRunning()
        else:
            return(0)

    def checkRMSPercentCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkRMSPercentRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkRMSPercentRunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkRMSPercentRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkRMSPercentRunning()
        else:
            return(0)

    def checkRMSPercentElasticpot():
        if Monitoring('elasticpot.py', 'running').checkRMSPercentRunning():
            return Monitoring('elasticpot.py', 'running').checkRMSPercentRunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkRMSPercentRunning():
            return Monitoring('elasticpot.py', 'sleeping').checkRMSPercentRunning()
        else:
            return(0)

    def checkRMSPercentRDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkRMSPercentRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkRMSPercentRunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkRMSPercentRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkRMSPercentRunning()
        else:
            return(0)


    # ==== CHECK HONEYPOT VMS PERCENTAGE ====    

    def checkVMSPercentDionaea():
        if Monitoring('dionaea', 'running').checkVMSPercentRunning():
            return Monitoring('dionaea', 'running').checkVMSPercentRunning()
        elif Monitoring('dionaea', 'sleeping').checkVMSPercentRunning():
            return Monitoring('dionaea', 'sleeping').checkVMSPercentRunning()
        else:
            return(0)

    def checkVMSPercentHoneytrap():
        if Monitoring('honeytrap', 'running').checkVMSPercentRunning():
            return Monitoring('honeytrap', 'running').checkVMSPercentRunning()
        elif Monitoring('honeytrap', 'sleeping').checkVMSPercentRunning():
            return Monitoring('honeytrap', 'sleeping').checkVMSPercentRunning()
        else:
            return(0)

    def checkVMSPercentGridpot():
        if Monitoring('conpot', 'running').checkVMSPercentRunning():
            return Monitoring('conpot', 'running').checkVMSPercentRunning()
        elif Monitoring('conpot', 'sleeping').checkVMSPercentRunning():
            return Monitoring('conpot', 'sleeping').checkVMSPercentRunning()
        else:
            return(0)

    def checkVMSPercentCowrie():
        if Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkVMSPercentRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'running').checkVMSPercentRunning()
        elif Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkVMSPercentRunning():
            return Monitoring('/cowrie/cowrie-env/bin/python3', 'sleeping').checkVMSPercentRunning()
        else:
            return(0)

    def checkVMSPercentElasticpot():
        if Monitoring('elasticpot.py', 'running').checkVMSPercentRunning():
            return Monitoring('elasticpot.py', 'running').checkVMSPercentRunning()
        elif Monitoring('elasticpot.py', 'sleeping').checkVMSPercentRunning():
            return Monitoring('elasticpot.py', 'sleeping').checkVMSPercentRunning()
        else:
            return(0)

    def checkVMSPercentRDPY():
        if Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkVMSPercentRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'running').checkVMSPercentRunning()
        elif Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkVMSPercentRunning():
            return Monitoring('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping').checkVMSPercentRunning()
        else:
            return(0)


    # ==== RUNNING LOGS MONITORING HONEYPOT ====
    
    logs_json = None
    def main():
        global logs_json
        logs_json = {
            "id_honeypot": str(uuid.uuid4()),
            "ip_address": Honeypot.ipAddress(),
            "hostname": socket.gethostname(),
            "honeypot_running": Honeypot.totalHoneypotRunning(),
            "dionaea_state": Honeypot.checkDionaea(),
            "dionaea_cpu": float("{:.2f}".format(Honeypot.checkCPUDionaea())),
            "dionaea_virtual_memory": float("{:.2f}".format(Honeypot.checkVirtualMemoryDionaea())),
            "dionaea_resident_memory": float("{:.2f}".format(Honeypot.checkResidentMemoryDionaea())),
            "dionaea_text_memory": float("{:.2f}".format(Honeypot.checkTextMemoryDionaea())),
            "dionaea_data_memory": float("{:.2f}".format(Honeypot.checkDataMemoryDionaea())),
            "dionaea_rms_percentage": float("{:.2f}".format(Honeypot.checkRMSPercentDionaea())),
            "dionaea_vms_percentage": float("{:.2f}".format(Honeypot.checkVMSPercentDionaea())),
            "honeytrap_state": Honeypot.checkHoneytrap(),
            "honeytrap_cpu": float("{:.2f}".format(Honeypot.checkCPUHoneytrap())),
            "honeytrap_virtual_memory": float("{:.2f}".format(Honeypot.checkVirtualMemoryHoneytrap())),
            "honeytrap_resident_memory": float("{:.2f}".format(Honeypot.checkResidentMemoryHoneytrap())),
            "honeytrap_text_memory": float("{:.2f}".format(Honeypot.checkTextMemoryHoneytrap())),
            "honeytrap_data_memory": float("{:.2f}".format(Honeypot.checkDataMemoryHoneytrap())),
            "honeytrap_rms_percentage": float("{:.2f}".format(Honeypot.checkRMSPercentHoneytrap())),
            "honeytrap_vms_percentage": float("{:.2f}".format(Honeypot.checkVMSPercentHoneytrap())),
            "gridpot_state": Honeypot.checkGridpot(),
            "gridpot_cpu": float("{:.2f}".format(Honeypot.checkCPUGridpot())),
            "gridpot_virtual_memory": float("{:.2f}".format(Honeypot.checkVirtualMemoryGridpot())),
            "gridpot_resident_memory": float("{:.2f}".format(Honeypot.checkResidentMemoryGridpot())),
            "gridpot_text_memory": float("{:.2f}".format(Honeypot.checkTextMemoryGridpot())),
            "gridpot_data_memory": float("{:.2f}".format(Honeypot.checkDataMemoryGridpot())),
            "gridpot_rms_percentage": float("{:.2f}".format(Honeypot.checkRMSPercentGridpot())),
            "gridpot_vms_percentage": float("{:.2f}".format(Honeypot.checkVMSPercentGridpot())),
            "cowrie_state": Honeypot.checkCowrie(),
            "cowrie_cpu": float("{:.2f}".format(Honeypot.checkCPUCowrie())),
            "cowrie_virtual_memory": float("{:.2f}".format(Honeypot.checkVirtualMemoryCowrie())),
            "cowrie_resident_memory": float("{:.2f}".format(Honeypot.checkResidentMemoryCowrie())),
            "cowrie_text_memory": float("{:.2f}".format(Honeypot.checkTextMemoryCowrie())),
            "cowrie_data_memory": float("{:.2f}".format(Honeypot.checkDataMemoryCowrie())),
            "cowrie_rms_percentage": float("{:.2f}".format(Honeypot.checkRMSPercentCowrie())),
            "cowrie_vms_percentage": float("{:.2f}".format(Honeypot.checkVMSPercentCowrie())),
            "elasticpot_state": Honeypot.checkElasticpot(),
            "elasticpot_cpu": float("{:.2f}".format(Honeypot.checkCPUElasticpot())),
            "elasticpot_virtual_memory": float("{:.2f}".format(Honeypot.checkVirtualMemoryElasticpot())),
            "elasticpot_resident_memory": float("{:.2f}".format(Honeypot.checkResidentMemoryElasticpot())),
            "elasticpot_text_memory": float("{:.2f}".format(Honeypot.checkTextMemoryElasticpot())),
            "elasticpot_data_memory": float("{:.2f}".format(Honeypot.checkDataMemoryElasticpot())),
            "elasticpot_rms_percentage": float("{:.2f}".format(Honeypot.checkRMSPercentElasticpot())),
            "elasticpot_vms_percentage": float("{:.2f}".format(Honeypot.checkVMSPercentElasticpot())),
            "rdpy_state": Honeypot.checkRDPY(),
            "rdpy_cpu": float("{:.2f}".format(Honeypot.checkCPURDPY())),
            "rdpy_virtual_memory": float("{:.2f}".format(Honeypot.checkVirtualMemoryRDPY())),
            "rdpy_resident_memory": float("{:.2f}".format(Honeypot.checkResidentMemoryRDPY())),
            "rdpy_text_memory": float("{:.2f}".format(Honeypot.checkTextMemoryRDPY())),
            "rdpy_data_memory": float("{:.2f}".format(Honeypot.checkDataMemoryRDPY())),
            "rdpy_rms_percentage": float("{:.2f}".format(Honeypot.checkRMSPercentRDPY())),
            "rdpy_vms_percentage": float("{:.2f}".format(Honeypot.checkVMSPercentRDPY())),
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
            result = client.publish(os.getenv('MQTT_TOPIC_HONEYPOT'), msg, qos=2)
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
 