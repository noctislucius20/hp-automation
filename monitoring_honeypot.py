import psutil
import schedule
import time
import json

def checkHoneypotRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkIfProcessRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkResidentMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()):
                return((proc.memory_info().rss) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkVirtualMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()):
                return((proc.memory_info().vms) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkTextMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()):
                return((proc.memory_info().text) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkDataMemoryRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()):
                return((proc.memory_info().data) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkMemoryPercentRunning(processName, status):
    for proc in psutil.process_iter():
        try:
            if (processName.lower() in proc.name().lower() and status.lower() in proc.status().lower()):
                return((proc.memory_percent()) / 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# def checking():
#     for proc in psutil.process_iter(['name', 'status']):
#         try:
#             print(proc.info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False   

def totalHoneypotRunning():
    if checkHoneypotRunning('twistd', 'running') and checkHoneypotRunning('dionaea', 'running'):
        return (2)
    elif checkHoneypotRunning('twistd', 'running') or checkHoneypotRunning('dionaea', 'running'):
        return (1)
    elif checkHoneypotRunning('twistd', 'sleeping') and checkHoneypotRunning('dionaea', 'sleeping'):
        return (2)
    elif checkHoneypotRunning('twistd', 'sleeping') or checkHoneypotRunning('dionaea', 'sleeping'):
        return (1)
    else:
        return (0) 

def checkCowrie():
    if checkIfProcessRunning('twistd', 'running'):
        return('Running')
    elif checkIfProcessRunning('twistd', 'sleeping'):
        return ('Sleeping')
    else:
        return('Not Running')

def checkDionaea():
    if checkIfProcessRunning('dionaea', 'running'):
        return('Running')
    elif checkIfProcessRunning('dionaea', 'sleeping'):
        return ('Sleeping')
    else:
        return('Not Running')

def checkResidentMemoryCowrie():
    if checkResidentMemoryRunning('twistd', 'running'):
        return checkResidentMemoryRunning('twistd', 'running')
    elif checkResidentMemoryRunning('twistd', 'sleeping'):
        return checkResidentMemoryRunning('twistd', 'sleeping')
    else:
        return(0)

def checkResidentMemoryDionaea():
    if checkResidentMemoryRunning('dionaea', 'running'):
        return checkResidentMemoryRunning('dionaea', 'running')
    elif checkResidentMemoryRunning('dionaea', 'sleeping'):
        return checkResidentMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkVirtualMemoryCowrie():
    if checkVirtualMemoryRunning('twistd', 'running'):
        return checkVirtualMemoryRunning('twistd', 'running')
    elif checkVirtualMemoryRunning('twistd', 'sleeping'):
        return checkVirtualMemoryRunning('twistd', 'sleeping')
    else:
        return(0)

def checkVirtualMemoryDionaea():
    if checkVirtualMemoryRunning('dionaea', 'running'):
        return checkVirtualMemoryRunning('dionaea', 'running')
    elif checkVirtualMemoryRunning('dionaea', 'sleeping'):
        return checkVirtualMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)

def checkTextMemoryCowrie():
    if checkTextMemoryRunning('twistd', 'running'):
        return checkTextMemoryRunning('twistd', 'running')
    elif checkTextMemoryRunning('twistd', 'sleeping'):
        return checkTextMemoryRunning('twistd', 'sleeping')
    else:
        return(0)

def checkTextMemoryDionaea():
    if checkTextMemoryRunning('dionaea', 'running'):
        return checkTextMemoryRunning('dionaea', 'running')
    elif checkTextMemoryRunning('dionaea', 'sleeping'):
        return checkTextMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)
    
def checkDataMemoryCowrie():
    if checkDataMemoryRunning('twistd', 'running'):
        return checkDataMemoryRunning('twistd', 'running')
    elif checkDataMemoryRunning('twistd', 'sleeping'):
        return checkDataMemoryRunning('twistd', 'sleeping')
    else:
        return(0)

def checkDataMemoryDionaea():
    if checkDataMemoryRunning('dionaea', 'running'):
        return checkDataMemoryRunning('dionaea', 'running')
    elif checkDataMemoryRunning('dionaea', 'sleeping'):
        return checkDataMemoryRunning('dionaea', 'sleeping')
    else:
        return(0)
    
def checkMemoryPercentCowrie():
    if checkMemoryPercentRunning('twistd', 'running'):
        return checkMemoryPercentRunning('twistd', 'running')
    elif checkMemoryPercentRunning('twistd', 'sleeping'):
        return checkMemoryPercentRunning('twistd', 'sleeping')
    else:
        return(0)

def checkMemoryPercentDionaea():
    if checkMemoryPercentRunning('dionaea', 'running'):
        return checkMemoryPercentRunning('dionaea', 'running')
    elif checkMemoryPercentRunning('dionaea', 'sleeping'):
        return checkMemoryPercentRunning('dionaea', 'sleeping')
    else:
        return(0)
        

def main():
    logs_json = {
        "honeypot_running": totalHoneypotRunning(),
        "cowrie": checkCowrie(),
        "cowrie_virtual_memory": float("{:.2f}".format(checkVirtualMemoryCowrie())),
        "cowrie_resident_memory": float("{:.2f}".format(checkResidentMemoryCowrie())),
        "cowrie_text_memory": float("{:.2f}".format(checkTextMemoryCowrie())),
        "cowrie_data_memory": float("{:.2f}".format(checkDataMemoryCowrie())),
        "cowrie_memory_percentage": float("{:.2f}".format(checkMemoryPercentCowrie())),
        "dionaea": checkDionaea(),
        "dionaea_virtual_memory": float("{:.2f}".format(checkVirtualMemoryDionaea())),
        "dionaea_resident_memory": float("{:.2f}".format(checkResidentMemoryDionaea())),
        "dionaea_text_memory": float("{:.2f}".format(checkTextMemoryDionaea())),
        "dionaea_data_memory": float("{:.2f}".format(checkDataMemoryDionaea())),
        "dionaea_memory_percentage": float("{:.2f}".format(checkMemoryPercentDionaea())),
    }

    print(logs_json)

    # with open('logs_honeypot.json', 'a+') as json_file:
    #     json.dump(logs_json, json_file)
    #     json_file.write("\n")

main()

# schedule.every(30).seconds.do(main)

# while True:
#     schedule.run_pending()
#     time.sleep(1)