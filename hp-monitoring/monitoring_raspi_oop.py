import psutil
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import psycopg2

class Monitoring:
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

class Raspi(Monitoring):
    def main():
        global logs_json
        logs_json = {
    #        "CPU_usage_percpu": cpu_usage_cpu,
            "CPU_usage": Monitoring.cpu_usage(),
            "CPU_frequency": float("{:.2f}".format(Monitoring.cpu_frequency())),
            # "CPU_temperature": cpu_temp,
            "CPU_count": Monitoring.cpu_count(),
            "RAM_total": float("{:.2f}".format(Monitoring.ram_total())),
            "RAM_usage": float("{:.2f}".format(Monitoring.ram_usage())),
            "RAM_available": float("{:.2f}".format(Monitoring.ram_available())),
            "RAM_percentage": Monitoring.ram_percent(),
            "swap_memory_total": float("{:.2f}".format(Monitoring.swap_memory_total())),
            "swap_memory_usage": float("{:.2f}".format(Monitoring.swap_memory_usage())),
            "swap_memory_free": float("{:.2f}".format(Monitoring.swap_memory_free())),
            "swap_memory_percentage": Monitoring.swap_memory_percentage(),
            # "disk_total": disk_tot,
            "network_packet_recv": Monitoring.network_packet_recv(),
            "network_packet_sent": Monitoring.network_packet_sent(),
            "datetime": datetime.now().isoformat()
            }
        
        return logs_json

class MQTT(Raspi):

    # ==== START MQTT CONNECTION & PUBLISH ====

    config_file = open('hp-monitoring/config.txt')
    config_dict = {}
    for lines in config_file:
        items = lines.split(': ', 1)
        config_dict[items[0]] = eval(items[1])

    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt.Client(MQTT.config_dict['MQTT_CLIENT_SENSOR'])
        client.on_connect = on_connect
        client.connect(MQTT.config_dict['MQTT_BROKER'], MQTT.config_dict['MQTT_PORT'])
        return client


    def publish(client):
        try:
            while True:
                time.sleep(30)
                msg = json.dumps(logs_json)
                result = client.publish(MQTT.config_dict['MQTT_TOPIC_SENSOR'], msg, qos=2)
                status = result[0]
                if status == 0:
                    print(msg)
                else:
                    print(f"Failed to send message to topic {MQTT.config_dict['MQTT_TOPIC_SENSOR']}")
        except:
            print("Failed to parse data")

    def message():
        try:
            connection = psycopg2.connect(user="postgres",
                                        password="scipio",
                                        host="10.33.102.212",
                                        port=54321,
                                        database="hp_automation")
            
            cursor = connection.cursor()
            print('Connected to PostgreSQL')

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)

    def run():
        client = MQTT.connect_mqtt()
        client.loop_start()
        Raspi.main()
        MQTT.publish(client)

if __name__ == '__main__':
    MQTT.run()