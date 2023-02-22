import psutil
import numpy as np
from datetime import datetime
import schedule
import time
import json

def checkHoneypotRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# def checkHoneypotRunningCMD(processCMD, status):
#     for proc in psutil.process_iter():
#         try:
#             if (processCMD in proc.cmdline() and status.lower() in proc.status().lower()):
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False

def checkIfProcessRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return(proc.status().capitalize())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkResidentMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_info().rss) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkVirtualMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_info().vms) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkTextMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_info().text) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkDataMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_info().data) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkMemoryPercentRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() or processName in proc.cmdline() and status.lower() in proc.status().lower()):
                return((proc.memory_percent(memtype='rss')) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checking():
    for proc in psutil.process_iter(['cmdline', 'status']):
        try:
            print(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False   


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
    elif False in list_honeypot_running:
        return(np.count_nonzero(list_honeypot_running == True))
    elif True in list_honeypot_sleeping:
        return(np.count_nonzero(list_honeypot_sleeping == True))
    elif False in list_honeypot_sleeping:
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

# CHECK HONEYPOT MEMORY PERCENTAGE    
def checkMemoryPercentDionaea():
    if checkMemoryPercentRunning('dionaea', 'running'):
        return checkMemoryPercentRunning('dionaea', 'running')
    elif checkMemoryPercentRunning('dionaea', 'sleeping'):
        return checkMemoryPercentRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkMemoryPercentHoneytrap():
    if checkMemoryPercentRunning('honeytrap', 'running'):
        return checkMemoryPercentRunning('honeytrap', 'running')
    elif checkMemoryPercentRunning('honeytrap', 'sleeping'):
        return checkMemoryPercentRunning('honeytrap', 'sleeping')
    else:
        return(0)

def checkMemoryPercentGridpot():
    if checkMemoryPercentRunning('conpot', 'running'):
        return checkMemoryPercentRunning('conpot', 'running')
    elif checkMemoryPercentRunning('conpot', 'sleeping'):
        return checkMemoryPercentRunning('conpot', 'sleeping')
    else:
        return(0)

def checkMemoryPercentCowrie():
    if checkMemoryPercentRunning('/cowrie/cowrie-env/bin/python3', 'running'):
        return checkMemoryPercentRunning('/cowrie/cowrie-env/bin/python3', 'running')
    elif checkMemoryPercentRunning('/cowrie/cowrie-env/bin/python3', 'sleeping'):
        return checkMemoryPercentRunning('/cowrie/cowrie-env/bin/python3', 'sleeping')
    else:
        return(0)

def checkMemoryPercentElasticpot():
    if checkMemoryPercentRunning('elasticpot.py', 'running'):
        return checkMemoryPercentRunning('elasticpot.py', 'running')
    elif checkMemoryPercentRunning('elasticpot.py', 'sleeping'):
        return checkMemoryPercentRunning('elasticpot.py', 'sleeping')
    else:
        return(0)

def checkMemoryPercentRDPY():
    if checkMemoryPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running'):
        return checkMemoryPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'running')
    elif checkMemoryPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping'):
        return checkMemoryPercentRunning('/rdpy/bin/rdpy-rdphoneypot.py', 'sleeping')
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
        "dionaea_memory_percentage": float("{:.2f}".format(checkMemoryPercentDionaea())),
        "honeytrap": checkHoneytrap(),
        "honeytrap_virtual_memory": float("{:.2f}".format(checkVirtualMemoryHoneytrap())),
        "honeytrap_resident_memory": float("{:.2f}".format(checkResidentMemoryHoneytrap())),
        "honeytrap_text_memory": float("{:.2f}".format(checkTextMemoryHoneytrap())),
        "honeytrap_data_memory": float("{:.2f}".format(checkDataMemoryHoneytrap())),
        "honeytrap_memory_percentage": float("{:.2f}".format(checkMemoryPercentHoneytrap())),
        "gridpot": checkGridpot(),
        "gridpot_virtual_memory": float("{:.2f}".format(checkVirtualMemoryGridpot())),
        "gridpot_resident_memory": float("{:.2f}".format(checkResidentMemoryGridpot())),
        "gridpot_text_memory": float("{:.2f}".format(checkTextMemoryGridpot())),
        "gridpot_data_memory": float("{:.2f}".format(checkDataMemoryGridpot())),
        "gridpot_memory_percentage": float("{:.2f}".format(checkMemoryPercentGridpot())),
        "cowrie": checkCowrie(),
        "cowrie_virtual_memory": float("{:.2f}".format(checkVirtualMemoryCowrie())),
        "cowrie_resident_memory": float("{:.2f}".format(checkResidentMemoryCowrie())),
        "cowrie_text_memory": float("{:.2f}".format(checkTextMemoryCowrie())),
        "cowrie_data_memory": float("{:.2f}".format(checkDataMemoryCowrie())),
        "cowrie_memory_percentage": float("{:.2f}".format(checkMemoryPercentCowrie())),
        "elasticpot": checkElasticpot(),
        "elasticpot_virtual_memory": float("{:.2f}".format(checkVirtualMemoryElasticpot())),
        "elasticpot_resident_memory": float("{:.2f}".format(checkResidentMemoryElasticpot())),
        "elasticpot_text_memory": float("{:.2f}".format(checkTextMemoryElasticpot())),
        "elasticpot_data_memory": float("{:.2f}".format(checkDataMemoryElasticpot())),
        "elasticpot_memory_percentage": float("{:.2f}".format(checkMemoryPercentElasticpot())),
        "rdpy": checkRDPY(),
        "rdpy_virtual_memory": float("{:.2f}".format(checkVirtualMemoryRDPY())),
        "rdpy_resident_memory": float("{:.2f}".format(checkResidentMemoryRDPY())),
        "rdpy_text_memory": float("{:.2f}".format(checkTextMemoryRDPY())),
        "rdpy_data_memory": float("{:.2f}".format(checkDataMemoryRDPY())),
        "rdpy_memory_percentage": float("{:.2f}".format(checkMemoryPercentRDPY())),
        "datetime": datetime.now().isoformat()
    }

    # print(logs_json)

    with open('logs_honeypot.json', 'a+') as json_file:
        json.dump(logs_json, json_file)
        json_file.write("\n")

# checking()
main()

schedule.every(30).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)