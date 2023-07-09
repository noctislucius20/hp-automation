from elasticsearch import Elasticsearch
import psycopg2
import time
import telebot
import os
import pytz
from datetime import datetime
from dotenv import load_dotenv


class Collector:
    connection = psycopg2.connect(user="postgres",
                                password="scipio",
                                host="10.33.102.212",
                                port=54321,
                                database="hp_automation")
    
    cursor = connection.cursor()
    print('Connected to PostgreSQL')

    client = Elasticsearch("http://10.33.102.212:9200")
    index_name = "monitoring_honeypot"
    print('Connected to Elasticsearch')

    timezone = pytz.timezone('Asia/Jakarta')

    # Define the mapping settings
    mapping_settings = {
        "properties": {
            "dionaea_state": {
                "type": "text",
                "fielddata": True
            },
            "honeytrap_state": {
                "type": "text",
                "fielddata": True
            },
            "cowrie_state": {
                "type": "text",
                "fielddata": True
            },
            "gridpot_state": {
                "type": "text",
                "fielddata": True
            },
            "elasticpot_state": {
                "type": "text",
                "fielddata": True
            },
            "rdpy_state": {
                "type": "text",
                "fielddata": True
            }
        }
    }
    client.indices.put_mapping(index=index_name, body=mapping_settings)

    def add_history_state():
        try:
            query = {
                'query': {
                    'match_all': {}
                },
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc"
                        }
                    }
                ],
                "size": 2
            }


            result = Collector.client.search(index=Collector.index_name, body=query)
            documents = result["hits"]["hits"] 
                
            honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
            ip_address = ""
            state_array = []
            rms_array = []
            cpu_array = []
            datetime_array = []
            get_id_honeypot_sensor = []

            for hp in honeypot:
                for document in documents:
                    message = eval(document["_source"]['message'])
                    ip_address = message["ip_address"]
                    honeypot_state = message[f"{hp}_state"]
                    honeypot_rms = message[f"{hp}_resident_memory"]
                    honeypot_cpu = message[f"{hp}_cpu"]
                    honeypot_datetime = message["datetime"]

                    state_array.append(honeypot_state)
                    rms_array.append(honeypot_rms)
                    cpu_array.append(honeypot_cpu)
                    datetime_array.append(honeypot_datetime)

            for index, value in enumerate(honeypot):
                Collector.cursor.execute(f"SELECT hs.id FROM honeypot_sensor hs JOIN honeypots h ON hs.honeypot_id = h.id JOIN sensors s ON hs.sensor_id = s.id WHERE h.name = '{value}' AND s.ip_address = '{ip_address}'")
                row = Collector.cursor.fetchall()

                if row:
                    id = row[0][0]
                else:
                    id = int(index) + 1

                get_id_honeypot_sensor.append(id)

            Collector.cursor.execute(f"SELECT id FROM sensors WHERE ip_address = '{ip_address}'")
            row_ip_address = Collector.cursor.fetchone()
            id_ip_address = row_ip_address[0]
            Collector.cursor.execute(f"SELECT dashboard_url FROM sensor_dashboards WHERE sensor_id = {id_ip_address}")
            row_dashboard_url = Collector.cursor.fetchone()
            dashboard_url = row_dashboard_url[0]

            if state_array is not None:
                for state, rms, cpu, time, hp, id_honeypot_sensor in zip(range(0, len(state_array), 2), range(0, len(rms_array), 2), range(0, len(cpu_array), 2), range(0, len(datetime_array), 2), honeypot, get_id_honeypot_sensor):
                    state_current = state_array[state]
                    state_late = state_array[state+1]

                    rms_current = rms_array[rms]
                    rms_late = rms_array[rms+1]

                    cpu_current = cpu_array[cpu]
                    cpu_late = cpu_array[cpu+1]
                    
                    time_current = datetime_array[time]
                    time_late = datetime_array[time+1]

                    if state_current != state_late:
                        if state_current == 'Not Running':
                            honeypot_status = f"{hp.capitalize()} is {state_current}"
                            status_code_id = 2
                            array = (id_honeypot_sensor, 'On', honeypot_status, status_code_id, time_current, rms_current, datetime.now(Collector.timezone).isoformat())
                            sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                            Collector.cursor.execute(sql_insert_query, array)
                            Collector.connection.commit()
                            print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                            send_alert = f"[Alerting Honeypot Status] \n\nSensor : {ip_address} \nCode : 400 \nDescription : Honeypot Off \nStatus Honeypot : {honeypot_status} \nResident Memory Size : {rms_current} KB \nCPU Percentage : {cpu_current}% \nDashboard URL: http://10.33.102.212:5601{dashboard_url} \nTimestamp : {time_current} \n\nMessage : Otomatisasi pengaktifan {hp.capitalize()} akan berlangsung dalam waktu 3-5 menit."
                            Bot.notifications(send_alert, "Alerting Honeypot Status")

                        else:
                            honeypot_status = f"{hp.capitalize()} is {state_current}"
                            status_code_id = 1
                            array = (id_honeypot_sensor, 'On', honeypot_status, status_code_id, time_current, rms_current, datetime.now(Collector.timezone).isoformat())
                            sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                            Collector.cursor.execute(sql_insert_query, array)
                            Collector.connection.commit()
                            print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                            send_alert = f"[Alerting Honeypot Status] \n\nSensor : {ip_address} \nCode : 200 \nDescription : Sensor & Honeypot On\nStatus Honeypot : {honeypot_status} \nResident Memory Size : {rms_current} KB \nCPU Percentage : {cpu_current}% \nDashboard URL: http://10.33.102.212:5601{dashboard_url} \nTimestamp : {time_current}"
                            Bot.notifications(send_alert, "Alerting Honeypot Status")

        except (Exception) as error:
            print(error)

    def add_history_health():
        try:
            query = {
                'query': {
                    'match_all': {}
                },
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc"
                        }
                    }
                ],
                "size": 1
            }


            result = Collector.client.search(index=Collector.index_name, body=query)
            documents = result["hits"]["hits"] 
                
            honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
            ip_address = ""
            time = ""
            state_array = []
            rms_array = []
            cpu_array = []
            get_id_honeypot_sensor = []

            for hp in honeypot:
                for document in documents:
                    message = eval(document["_source"]['message'])
                    ip_address = message["ip_address"]
                    honeypot_state = message[f"{hp}_state"]
                    honeypot_rms = message[f"{hp}_resident_memory"]
                    honeypot_cpu = message[f"{hp}_cpu"]
                    time = message["datetime"]

                    state_array.append(honeypot_state)
                    rms_array.append(honeypot_rms)
                    cpu_array.append(honeypot_cpu)

            for index, value in enumerate(honeypot):
                Collector.cursor.execute(f"SELECT hs.id FROM honeypot_sensor hs JOIN honeypots h ON hs.honeypot_id = h.id JOIN sensors s ON hs.sensor_id = s.id WHERE h.name = '{value}' AND s.ip_address = '{ip_address}'")
                row = Collector.cursor.fetchall()

                if row:
                    id = row[0][0]
                else:
                    id = int(index) + 1

                get_id_honeypot_sensor.append(id)

            Collector.cursor.execute(f"SELECT id FROM sensors WHERE ip_address = '{ip_address}'")
            row_ip_address = Collector.cursor.fetchone()
            id_ip_address = row_ip_address[0]
            Collector.cursor.execute(f"SELECT dashboard_url FROM sensor_dashboards WHERE sensor_id = {id_ip_address}")
            row_dashboard_url = Collector.cursor.fetchone()
            dashboard_url = row_dashboard_url[0]

            if cpu_array[0] > 25 and rms_array[1] > 70000:
                honeypot_status = f"{honeypot[0].capitalize()} is Unhealthy"
                status_code_id = 3
                array = (get_id_honeypot_sensor[0], 'On', honeypot_status, status_code_id, time, rms_array[0], datetime.now(Collector.timezone).isoformat())
                sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                Collector.cursor.execute(sql_insert_query, array)
                Collector.connection.commit()
                print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                send_alert = f"[Alerting Honeypot Resource] \n\nSensor : {ip_address} \nCode : 401 \nDescription : Honeypot is Unhealthy \nStatus Honeypot : {honeypot_status} \nResident Memory Size : {rms_array[0]} KB \nCPU Percentage : {cpu_array[0]}% \nDashboard URL: http://10.33.102.212:5601{dashboard_url} \nTimestamp : {time}"
                Bot.notifications(send_alert, "Honeypot Resource Alert")      

            if cpu_array[1] > 25 and rms_array[1] > 80000:
                honeypot_status = f"{honeypot[1].capitalize()} is Unhealthy"
                status_code_id = 3
                array = (get_id_honeypot_sensor[1], 'On', honeypot_status, status_code_id, time, rms_array[1], datetime.now(Collector.timezone).isoformat())
                sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                Collector.cursor.execute(sql_insert_query, array)
                Collector.connection.commit()
                print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                send_alert = f"[Alerting Honeypot Resource] \n\nSensor : {ip_address} \nCode : 401 \nDescription : Honeypot is Unhealthy \nStatus Honeypot : {honeypot_status} \nResident Memory Size : {rms_array[1]} KB \nCPU Percentage : {cpu_array[1]}% \nDashboard URL: http://10.33.102.212:5601{dashboard_url} \nTimestamp : {time}"      

            if cpu_array[2] > 25 and rms_array[2] > 125000:
                honeypot_status = f"{honeypot[2].capitalize()} is Unhealthy"
                status_code_id = 3
                array = (get_id_honeypot_sensor[2], 'On', honeypot_status, status_code_id, time, rms_array[2], datetime.now(Collector.timezone).isoformat())
                sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                Collector.cursor.execute(sql_insert_query, array)
                Collector.connection.commit()
                print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                send_alert = f"[Alerting Honeypot Resource] \n\nSensor : {ip_address} \nCode : 401 \nDescription : Honeypot is Unhealthy \nStatus Honeypot : {honeypot_status} \nResident Memory Size : {rms_array[2]} KB \nCPU Percentage : {cpu_array[2]}% \nDashboard URL: http://10.33.102.212:5601{dashboard_url} \nTimestamp : {time}"
                Bot.notifications(send_alert, "Honeypot Resource Alert")           

            if cpu_array[4] > 25 and rms_array[4] > 67000:
                honeypot_status = f"{honeypot[4].capitalize()} is Unhealthy"
                status_code_id = 3
                array = (get_id_honeypot_sensor[4], 'On', honeypot_status, status_code_id, time, rms_array[4], datetime.now(Collector.timezone).isoformat())
                sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                Collector.cursor.execute(sql_insert_query, array)
                Collector.connection.commit()
                print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                send_alert = f"[Alerting Honeypot Resource] \n\nSensor : {ip_address} \nCode : 401 \nDescription : Honeypot is Unhealthy \nStatus Honeypot : {honeypot_status} \nResident Memory Size : {rms_array[4]} KB \nCPU Percentage : {cpu_array[4]}% \nDashboard URL: http://10.33.102.212:5601{dashboard_url} \nTimestamp : {time}"
                Bot.notifications(send_alert, "Honeypot Resource Alert")    
    
        except (Exception) as error:
            print(error)


class Bot(Collector):
    def notifications(message, alerting):
        try:
            API_KEY = os.getenv('API_KEY')
            bot = telebot.TeleBot("6289233331:AAG_l-CfrztpTtYs_9o6ZtKo2adniEi8_Ig")
            chat_id = -963526950

            bot.send_message(chat_id=chat_id, text=message)
            print(f"Message sent to Bot Telegram {alerting} at {datetime.now(Collector.timezone)}")

        except (Exception) as error:
            print(error)


class Main(Bot):
    def run():
        Collector.add_history_state()
        Collector.add_history_health()


if __name__ == '__main__':
    while True:
        Main.run()
        time.sleep(5)