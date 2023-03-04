import socket
import psutil
import numpy as np
from datetime import datetime
import schedule
import time
import json

# def hostname():
#     hostname = socket.gethostname()
#     ip_address = socket.gethostbyname(hostname)
#     print(hostname)
#     print(ip_address)

def checkHoneypotRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkIfProcessRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return(proc.status().capitalize())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkResidentMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_info().rss) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkVirtualMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()) or processName in proc.cmdline() and status.lower() in proc.status().lower():
                return((proc.memory_info().vms) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkTextMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_info().text) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkDataMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_info().data) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkRMSPercentRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_percent(memtype='rss')))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkVMSPercentRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_percent(memtype='vms')))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# def checking():
#     for proc in psutil.process_iter(['cmdline', 'status']):
#         try:
#             print(proc.info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False   


# CHECK HONEYPOT RUNNING
def totalHoneypotRunning():
    dionaea_running = checkHoneypotRunning('dionaea', 'running')
    dionaea_sleeping = checkHoneypotRunning('dionaea', 'sleeping')
    honeytrap_running = checkHoneypotRunning('honeytrap', 'running')
    honeytrap_sleeping = checkHoneypotRunning('honeytrap', 'sleeping')
    gridpot_running = checkHoneypotRunning('conpot', 'running')
    gridpot_sleeping = checkHoneypotRunning('conpot', 'sleeping')
    cowrie_running = checkHoneypotRunning('/cowrie/cowrie-env/bin/python3', 'running')
    cowrie_sleeping = checkHoneypotRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    elasticpot_running = checkHoneypotRunning('elasticpot.py', 'running')
    elasticpot_sleeping = checkHoneypotRunning('elasticpot.py', 'sleeping')
    rdpy_running = checkHoneypotRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    rdpy_sleeping = checkHoneypotRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')

    list_honeypot_running = np.array([dionaea_running, honeytrap_running, gridpot_running, cowrie_running, elasticpot_running, rdpy_running])
    list_honeypot_sleeping = np.array([dionaea_sleeping, honeytrap_sleeping, gridpot_sleeping, cowrie_sleeping, elasticpot_sleeping, rdpy_sleeping])

    if True in list_honeypot_running:
        return(np.count_nonzero(list_honeypot_running == True))
    elif True in list_honeypot_sleeping:
        return(np.count_nonzero(list_honeypot_sleeping == True))
    else:
        return(0)


# CHECK HONEYPOT STATUS
def checkDionaea():
    if checkIfProcessRunning('dionaea', 'running'):
        return(checkIfProcessRunning('dionaea', 'running'))
    elif checkIfProcessRunning('dionaea', 'sleeping'):
        return(checkIfProcessRunning('dionaea', 'sleeping'))
    else:
        return('Not Running')

def checkHoneytrap():
    if checkIfProcessRunning('honeytrap', 'running'):
        return checkIfProcessRunning('honeytrap', 'running')
    elif checkIfProcessRunning('honeytrap', 'sleeping'):
        return checkIfProcessRunning('honeytrap', 'sleeping')
    else:
        return('Not Running')

def checkGridpot():
    if checkIfProcessRunning('conpot', 'running'):
        return checkIfProcessRunning('conpot', 'running')
    elif checkIfProcessRunning('conpot', 'sleeping'):
        return checkIfProcessRunning('conpot', 'sleeping')
    else:
        return('Not Running')

def checkCowrie():
    if checkIfProcessRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return (checkIfProcessRunning('/cowrie/cowrie-env/bin/python3', 'running'))
    elif checkIfProcessRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return (checkIfProcessRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'))
    else:
        return('Not Running')

def checkElasticpot():
    if checkIfProcessRunning('elasticpot.py', 'running'):
        return (checkIfProcessRunning('elasticpot.py', 'running'))
    elif checkIfProcessRunning('elasticpot.py', 'sleeping'):
        return (checkIfProcessRunning('elasticpot.py', 'sleeping'))
    else:
        return('Not Running')

def checkRDPY():
    if checkIfProcessRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return (checkIfProcessRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'))
    elif checkIfProcessRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return (checkIfProcessRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'))
    else:
        return('Not Running')


# CHECK HONEYPOT RMS
def checkResidentMemoryDionaea():
    if checkResidentMemoryRunning('dionaea', 'running'):
        return checkResidentMemoryRunning('dionaea', 'running')
    elif checkResidentMemoryRunning('dionaea', 'sleeping'):
        return checkResidentMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkResidentMemoryHoneytrap():
    if checkResidentMemoryRunning('honeytrap', 'running'):
        return checkResidentMemoryRunning('honeytrap', 'running')
    elif checkResidentMemoryRunning('honeytrap', 'sleeping'):
        return checkResidentMemoryRunning('honeytrap', 'sleeping')
    else:
        return(0)

def checkResidentMemoryGridpot():
    if checkResidentMemoryRunning('conpot', 'running'):
        return checkResidentMemoryRunning('conpot', 'running')
    elif checkResidentMemoryRunning('conpot', 'sleeping'):
        return checkResidentMemoryRunning('conpot', 'sleeping')
    else:
        return(0)

def checkResidentMemoryCowrie():
    if checkResidentMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return checkResidentMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running')
    elif checkResidentMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return checkResidentMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    else:
        return(0)

def checkResidentMemoryElasticpot():
    if checkResidentMemoryRunning('elasticpot.py', 'running'):
        return checkResidentMemoryRunning('elasticpot.py', 'running')
    elif checkResidentMemoryRunning('elasticpot.py', 'sleeping'):
        return checkResidentMemoryRunning('elasticpot.py', 'sleeping')
    else:
        return(0)

def checkResidentMemoryRDPY():
    if checkResidentMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return checkResidentMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    elif checkResidentMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return checkResidentMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')
    else:
        return(0)


# CHECK HONEYPOT VMS
def checkVirtualMemoryDionaea():
    if checkVirtualMemoryRunning('dionaea', 'running'):
        return checkVirtualMemoryRunning('dionaea', 'running')
    elif checkVirtualMemoryRunning('dionaea', 'sleeping'):
        return checkVirtualMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkVirtualMemoryHoneytrap():
    if checkVirtualMemoryRunning('honeytrap', 'running'):
        return checkVirtualMemoryRunning('honeytrap', 'running')
    elif checkVirtualMemoryRunning('honeytrap', 'sleeping'):
        return checkVirtualMemoryRunning('honeytrap', 'sleeping')
    else:
        return(0)

def checkVirtualMemoryGridpot():
    if checkVirtualMemoryRunning('conpot', 'running'):
        return checkVirtualMemoryRunning('conpot', 'running')
    elif checkVirtualMemoryRunning('conpot', 'sleeping'):
        return checkVirtualMemoryRunning('conpot', 'sleeping')
    else:
        return(0)

def checkVirtualMemoryCowrie():
    if checkVirtualMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return checkVirtualMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running')
    elif checkVirtualMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return checkVirtualMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    else:
        return(0)

def checkVirtualMemoryElasticpot():
    if checkVirtualMemoryRunning('elasticpot.py', 'running'):
        return checkVirtualMemoryRunning('elasticpot.py', 'running')
    elif checkVirtualMemoryRunning('elasticpot.py', 'sleeping'):
        return checkVirtualMemoryRunning('elasticpot.py', 'sleeping')
    else:
        return(0)

def checkVirtualMemoryRDPY():
    if checkVirtualMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return checkVirtualMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    elif checkVirtualMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return checkVirtualMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')
    else:
        return(0)


# CHECK HONEYPOT TMS
def checkTextMemoryDionaea():
    if checkTextMemoryRunning('dionaea', 'running'):
        return checkTextMemoryRunning('dionaea', 'running')
    elif checkTextMemoryRunning('dionaea', 'sleeping'):
        return checkTextMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkTextMemoryHoneytrap():
    if checkTextMemoryRunning('honeytrap', 'running'):
        return checkTextMemoryRunning('honeytrap', 'running')
    elif checkTextMemoryRunning('honeytrap', 'sleeping'):
        return checkTextMemoryRunning('honeytrap', 'sleeping')
    else:
        return(0)

def checkTextMemoryGridpot():
    if checkTextMemoryRunning('conpot', 'running'):
        return checkTextMemoryRunning('conpot', 'running')
    elif checkTextMemoryRunning('conpot', 'sleeping'):
        return checkTextMemoryRunning('conpot', 'sleeping')
    else:
        return(0)

def checkTextMemoryCowrie():
    if checkTextMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return checkTextMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running')
    elif checkTextMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return checkTextMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    else:
        return(0)

def checkTextMemoryElasticpot():
    if checkTextMemoryRunning('elasticpot.py', 'running'):
        return checkTextMemoryRunning('elasticpot.py', 'running')
    elif checkTextMemoryRunning('elasticpot.py', 'sleeping'):
        return checkTextMemoryRunning('elasticpot.py', 'sleeping')
    else:
        return(0)

def checkTextMemoryRDPY():
    if checkTextMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return checkTextMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    elif checkTextMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return checkTextMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')
    else:
        return(0)


#CHECK HONEYPOT DATA MEMORY    
def checkDataMemoryDionaea():
    if checkDataMemoryRunning('dionaea', 'running'):
        return checkDataMemoryRunning('dionaea', 'running')
    elif checkDataMemoryRunning('dionaea', 'sleeping'):
        return checkDataMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkDataMemoryHoneytrap():
    if checkDataMemoryRunning('honeytrap', 'running'):
        return checkDataMemoryRunning('honeytrap', 'running')
    elif checkDataMemoryRunning('honeytrap', 'sleeping'):
        return checkDataMemoryRunning('honeytrap', 'sleeping')
    else:
        return(0)

def checkDataMemoryGridpot():
    if checkDataMemoryRunning('conpot', 'running'):
        return checkDataMemoryRunning('conpot', 'running')
    elif checkDataMemoryRunning('conpot', 'sleeping'):
        return checkDataMemoryRunning('conpot', 'sleeping')
    else:
        return(0)

def checkDataMemoryCowrie():
    if checkDataMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return checkDataMemoryRunning('/cowrie/cowrie-env/bin/python3', 'running')
    elif checkDataMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return checkDataMemoryRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    else:
        return(0)

def checkDataMemoryElasticpot():
    if checkDataMemoryRunning('elasticpot.py', 'running'):
        return checkDataMemoryRunning('elasticpot.py', 'running')
    elif checkDataMemoryRunning('elasticpot.py', 'sleeping'):
        return checkDataMemoryRunning('elasticpot.py', 'sleeping')
    else:
        return(0)

def checkDataMemoryRDPY():
    if checkDataMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return checkDataMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    elif checkDataMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return checkDataMemoryRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')
    else:
        return(0)

# CHECK HONEYPOT RMS PERCENTAGE    
def checkRMSPercentDionaea():
    if checkRMSPercentRunning('dionaea', 'running'):
        return checkRMSPercentRunning('dionaea', 'running')
    elif checkRMSPercentRunning('dionaea', 'sleeping'):
        return checkRMSPercentRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkRMSPercentHoneytrap():
    if checkRMSPercentRunning('honeytrap', 'running'):
        return checkRMSPercentRunning('honeytrap', 'running')
    elif checkRMSPercentRunning('honeytrap', 'sleeping'):
        return checkRMSPercentRunning('honeytrap', 'sleeping')
    else:
        return(0)

def checkRMSPercentGridpot():
    if checkRMSPercentRunning('conpot', 'running'):
        return checkRMSPercentRunning('conpot', 'running')
    elif checkRMSPercentRunning('conpot', 'sleeping'):
        return checkRMSPercentRunning('conpot', 'sleeping')
    else:
        return(0)

def checkRMSPercentCowrie():
    if checkRMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return checkRMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'running')
    elif checkRMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return checkRMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    else:
        return(0)

def checkRMSPercentElasticpot():
    if checkRMSPercentRunning('elasticpot.py', 'running'):
        return checkRMSPercentRunning('elasticpot.py', 'running')
    elif checkRMSPercentRunning('elasticpot.py', 'sleeping'):
        return checkRMSPercentRunning('elasticpot.py', 'sleeping')
    else:
        return(0)

def checkRMSPercentRDPY():
    if checkRMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return checkRMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    elif checkRMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return checkRMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')
    else:
        return(0)

# CHECK HONEYPOT VMS PERCENTAGE    
def checkVMSPercentDionaea():
    if checkVMSPercentRunning('dionaea', 'running'):
        return checkVMSPercentRunning('dionaea', 'running')
    elif checkVMSPercentRunning('dionaea', 'sleeping'):
        return checkVMSPercentRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkVMSPercentHoneytrap():
    if checkVMSPercentRunning('honeytrap', 'running'):
        return checkVMSPercentRunning('honeytrap', 'running')
    elif checkVMSPercentRunning('honeytrap', 'sleeping'):
        return checkVMSPercentRunning('honeytrap', 'sleeping')
    else:
        return(0)

def checkVMSPercentGridpot():
    if checkVMSPercentRunning('conpot', 'running'):
        return checkVMSPercentRunning('conpot', 'running')
    elif checkVMSPercentRunning('conpot', 'sleeping'):
        return checkVMSPercentRunning('conpot', 'sleeping')
    else:
        return(0)

def checkVMSPercentCowrie():
    if checkVMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return checkVMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'running')
    elif checkVMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return checkVMSPercentRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    else:
        return(0)

def checkVMSPercentElasticpot():
    if checkVMSPercentRunning('elasticpot.py', 'running'):
        return checkVMSPercentRunning('elasticpot.py', 'running')
    elif checkVMSPercentRunning('elasticpot.py', 'sleeping'):
        return checkVMSPercentRunning('elasticpot.py', 'sleeping')
    else:
        return(0)

def checkVMSPercentRDPY():
    if checkVMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return checkVMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    elif checkVMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return checkVMSPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')
    else:
        return(0)
        
# MAIN FUNCTION
def main():
    logs_json = {
        "honeypot_running": totalHoneypotRunning(),
        "dionaea": checkDionaea(),
        "dionaea_virtual_memory": float("{:.2f}".format(checkVirtualMemoryDionaea())),
        "dionaea_resident_memory": float("{:.2f}".format(checkResidentMemoryDionaea())),
        "dionaea_text_memory": float("{:.2f}".format(checkTextMemoryDionaea())),
        "dionaea_data_memory": float("{:.2f}".format(checkDataMemoryDionaea())),
        "dionaea_rms_percentage": float("{:.2f}".format(checkRMSPercentDionaea())),
        "dionaea_vms_percentage": float("{:.2f}".format(checkVMSPercentDionaea())),
        "honeytrap": checkHoneytrap(),
        "honeytrap_virtual_memory": float("{:.2f}".format(checkVirtualMemoryHoneytrap())),
        "honeytrap_resident_memory": float("{:.2f}".format(checkResidentMemoryHoneytrap())),
        "honeytrap_text_memory": float("{:.2f}".format(checkTextMemoryHoneytrap())),
        "honeytrap_data_memory": float("{:.2f}".format(checkDataMemoryHoneytrap())),
        "honeytrap_rms_percentage": float("{:.2f}".format(checkRMSPercentHoneytrap())),
        "honeytrap_vms_percentage": float("{:.2f}".format(checkVMSPercentHoneytrap())),
        "gridpot": checkGridpot(),
        "gridpot_virtual_memory": float("{:.2f}".format(checkVirtualMemoryGridpot())),
        "gridpot_resident_memory": float("{:.2f}".format(checkResidentMemoryGridpot())),
        "gridpot_text_memory": float("{:.2f}".format(checkTextMemoryGridpot())),
        "gridpot_data_memory": float("{:.2f}".format(checkDataMemoryGridpot())),
        "gridpot_rms_percentage": float("{:.2f}".format(checkRMSPercentGridpot())),
        "gridpot_vms_percentage": float("{:.2f}".format(checkVMSPercentGridpot())),
        "cowrie": checkCowrie(),
        "cowrie_virtual_memory": float("{:.2f}".format(checkVirtualMemoryCowrie())),
        "cowrie_resident_memory": float("{:.2f}".format(checkResidentMemoryCowrie())),
        "cowrie_text_memory": float("{:.2f}".format(checkTextMemoryCowrie())),
        "cowrie_data_memory": float("{:.2f}".format(checkDataMemoryCowrie())),
        "cowrie_rms_percentage": float("{:.2f}".format(checkRMSPercentCowrie())),
        "cowrie_vms_percentage": float("{:.2f}".format(checkVMSPercentCowrie())),
        "elasticpot": checkElasticpot(),
        "elasticpot_virtual_memory": float("{:.2f}".format(checkVirtualMemoryElasticpot())),
        "elasticpot_resident_memory": float("{:.2f}".format(checkResidentMemoryElasticpot())),
        "elasticpot_text_memory": float("{:.2f}".format(checkTextMemoryElasticpot())),
        "elasticpot_data_memory": float("{:.2f}".format(checkDataMemoryElasticpot())),
        "elasticpot_rms_percentage": float("{:.2f}".format(checkRMSPercentElasticpot())),
        "elasticpot_vms_percentage": float("{:.2f}".format(checkVMSPercentElasticpot())),
        "rdpy": checkRDPY(),
        "rdpy_virtual_memory": float("{:.2f}".format(checkVirtualMemoryRDPY())),
        "rdpy_resident_memory": float("{:.2f}".format(checkResidentMemoryRDPY())),
        "rdpy_text_memory": float("{:.2f}".format(checkTextMemoryRDPY())),
        "rdpy_data_memory": float("{:.2f}".format(checkDataMemoryRDPY())),
        "rdpy_rms_percentage": float("{:.2f}".format(checkRMSPercentRDPY())),
        "rdpy_vms_percentage": float("{:.2f}".format(checkVMSPercentRDPY())),
        "datetime": datetime.now().isoformat()
    }

    # print(logs_json)

    with open('hp-monitoring/logs_honeypot.json', 'a+') as json_file:
        json.dump(logs_json, json_file)
        json_file.write("\n")

# checking()
main()
schedule.every(30).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)