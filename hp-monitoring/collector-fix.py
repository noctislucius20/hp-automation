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
    index_honeypot = "monitoring_honeypot"
    index_sensor = "monitoring_sensor"
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
    client.indices.put_mapping(index=index_honeypot, body=mapping_settings)

    def add_history_status():
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


            result_honeypot = Collector.client.search(index=Collector.index_honeypot, body=query)
            documents_honeypot = result_honeypot["hits"]["hits"]
                
            honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
            ip_address = ""
            time = ""
            health_status = ""
            state_array = []
            rms_array = []
            cpu_array = []
            storage_array = []
            get_id_honeypot_sensor = []

            for hp in honeypot:
                for document in documents_honeypot:
                    message = eval(document["_source"]['message'])
                    ip_address = message["ip_address"]
                    honeypot_state = message[f"{hp}_state"]
                    honeypot_rms = message[f"{hp}_resident_memory"]
                    honeypot_cpu = message[f"{hp}_cpu"]
                    honeypot_storage = message[f"{hp}_storage"]
                    time = message["datetime"]

                    state_array.append(honeypot_state)
                    rms_array.append(honeypot_rms)
                    cpu_array.append(honeypot_cpu)
                    storage_array.append(honeypot_storage)

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

            for state, rms, cpu, storage, hp, id_honeypot_sensor in zip(state_array, rms_array, cpu_array, storage_array, honeypot, get_id_honeypot_sensor):
                Collector.cursor.execute("SELECT COUNT(*) FROM history")
                result = Collector.cursor.fetchone()

                state_current = f"{hp.capitalize()} is {state}"           
                    
                query = f"SELECT h.honeypot_status FROM history h JOIN honeypot_sensor hs ON h.honeypot_sensor_id = hs.id JOIN honeypots hp ON hs.honeypot_id = hp.id JOIN sensors s ON hs.sensor_id = s.id WHERE hp.name = '{hp}' AND s.ip_address = '{ip_address}' ORDER BY h.created_at DESC LIMIT 1;"
                Collector.cursor.execute(query)
                row = Collector.cursor.fetchall()

                if result[0] > len(honeypot) and row:
                    state_late = row[0][0]

                    if state_current != state_late:
                        if state_current == f"{hp.capitalize()} is Not Running":
                            honeypot_status = state_current
                            status_code_id = 2
                            array = (id_honeypot_sensor, 'On', honeypot_status, status_code_id, time, rms, datetime.now(Collector.timezone).isoformat())
                            sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                            Collector.cursor.execute(sql_insert_query, array)
                            Collector.connection.commit()
                            print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                            send_alert = f"*[Alerting Honeypot Status]* \n\n*Device* : {ip_address} \n*Code* : 400 \n*Connection Status* : Connected \n*Description* : Device On & Honeypot Off \n\n*Status Honeypot* : {honeypot_status} \n*Memory Size* : {rms} MB \n*Storage Size* : {storage} MB \n*CPU Percentage* : {cpu}% \n\n*Dashboard URL* : http://10.33.102.212:5601{dashboard_url} \n*Timestamp* : {time} \n\n*Message* : Otomatisasi pengaktifan {hp.capitalize()} akan berlangsung dalam waktu 3-5 menit."
                            Bot.notifications(send_alert, "Alerting Honeypot Status")

                        else:
                            honeypot_status = state_current
                            status_code_id = 1
                            array = (id_honeypot_sensor, 'On', honeypot_status, status_code_id, time, rms, datetime.now(Collector.timezone).isoformat())
                            sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                            Collector.cursor.execute(sql_insert_query, array)
                            Collector.connection.commit()
                            print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                            send_alert = f"*[Alerting Honeypot Status]* \n\n*Device* : {ip_address} \n*Code* : 200 \n*Connection Status* : Connected \n*Description* : Device & Honeypot On \n\n*Status Honeypot* : {honeypot_status} \n*Honeypot Health Status* : {health_status} \n*Memory Size* : {rms} MB \n*Storage Size* : {storage} MB \n*CPU Percentage* : {cpu}% \n\n*Dashboard URL* : http://10.33.102.212:5601{dashboard_url} \n*Timestamp* : {time}"
                            Bot.notifications(send_alert, "Alerting Honeypot Status")

                else:
                    if state == 'Not Running':
                        honeypot_status = f"{hp.capitalize()} is {state}"
                        status_code_id = 2
                        array = (id_honeypot_sensor, 'On', honeypot_status, status_code_id, time, rms, datetime.now(Collector.timezone).isoformat())
                        sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                        Collector.cursor.execute(sql_insert_query, array)
                        Collector.connection.commit()
                        print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                        send_alert = f"*[Alerting Honeypot Status]* \n\n*Device* : {ip_address} \n*Code* : 400 \n*Connection Status* : Connected \n*Description* : Device On & Honeypot Off \n\n*Status Honeypot* : {honeypot_status} \n*Memory Size* : {rms} MB \n*Storage Size* : {storage} MB \n*CPU Percentage* : {cpu}% \n\n*Dashboard URL* : http://10.33.102.212:5601{dashboard_url} \n*Timestamp* : {time} \n\n*Message* : Otomatisasi pengaktifan {hp.capitalize()} akan berlangsung dalam waktu 3-5 menit."
                        Bot.notifications(send_alert, "Alerting Honeypot Status")

                    else:
                        honeypot_status = f"{hp.capitalize()} is {state}"
                        status_code_id = 1
                        array = (id_honeypot_sensor, 'On', honeypot_status, status_code_id, time, rms, datetime.now(Collector.timezone).isoformat())
                        sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                        Collector.cursor.execute(sql_insert_query, array)
                        Collector.connection.commit()
                        print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now(Collector.timezone).isoformat()}")

                        send_alert = f"*[Alerting Honeypot Status]* \n\n*Device* : {ip_address} \n*Connection Status* : Connected \n*Code* : 200 \n*Description* : Device & Honeypot On \n\n*Status Honeypot* : {honeypot_status} \n*Honeypot Health Status* : {health_status} \n*Memory Size* : {rms} MB \n*Storage Size* : {storage} MB \n*CPU Percentage* : {cpu}% \n\n*Dashboard URL* : http://10.33.102.212:5601{dashboard_url} \n*Timestamp* : {time}"
                        Bot.notifications(send_alert, "Alerting Honeypot Status")
  
    
        except (Exception) as error:
            print(error)

class Bot(Collector):
    def notifications(message, alerting):
        try:
            API_KEY = os.getenv('API_KEY')
            bot = telebot.TeleBot("6289233331:AAG_l-CfrztpTtYs_9o6ZtKo2adniEi8_Ig")
            chat_id = -963526950

            bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            print(f"Message sent to Bot Telegram {alerting} at {datetime.now(Collector.timezone)}")

        except (Exception) as error:
            print(error)


class Main(Bot):
    def run():
        Collector.add_history_status()

if __name__ == '__main__':
    Main.run()