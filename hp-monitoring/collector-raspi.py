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
            result_sensor = Collector.client.search(index=Collector.index_sensor, body=query)

            documents_honeypot = result_honeypot["hits"]["hits"] 
            documents_sensor = result_sensor["hits"]["hits"] 
                
            honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
            ip_address = ""
            time = ""
            state_array = []
            rms_array = []
            cpu_array = []
            storage_usage = 0.0
            storage_total = 0.0
            get_id_honeypot_sensor = []

            for hp in honeypot:
                for document in documents_honeypot:
                    message = eval(document["_source"]['message'])
                    ip_address = message["ip_address"]
                    honeypot_state = message[f"{hp}_state"]
                    honeypot_rms = message[f"{hp}_resident_memory"]
                    honeypot_cpu = message[f"{hp}_cpu"]
                    time = message["datetime"]

                    state_array.append(honeypot_state)
                    rms_array.append(honeypot_rms)
                    cpu_array.append(honeypot_cpu)

            for document in documents_sensor:
                message = eval(document["_source"]['message'])
                ram_usage = message["RAM_usage"]
                storage_usage = message["storage_used"]
                storage_total = message["storage_total"]

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

            if storage_usage > (0.25 * storage_total):
                send_alert = f"*[Alerting Raspberry Pi Resource]* \n\n*Device* : {ip_address} \n*Code* : 402 \n*Connection Status* : Connected \n*Description* : Device is Unhealthy \n*Storage Size* : {storage_usage} \n*Message* : Terjadi Kenaikan Storage Melebihi 25% \n*Timestamp* : {time}"
                Bot.notifications(send_alert, "Honeypot Resource Alert")   
            elif storage_usage > (0.5 * storage_total):
                send_alert = f"*[Alerting Raspberry Pi Resource]* \n\n*Device* : {ip_address} \n*Code* : 402 \n*Connection Status* : Connected \n*Description* : Device is Unhealthy \n*Storage Size* : {storage_usage} \n*Message* : Terjadi Kenaikan Storage Melebihi 50% \n*Timestamp* : {time}"
                Bot.notifications(send_alert, "Honeypot Resource Alert")
            elif storage_usage > (0.75 * storage_total):
                send_alert = f"*[Alerting Raspberry Pi Resource]* \n\n*Device* : {ip_address} \n*Code* : 402 \n*Connection Status* : Connected \n*Description* : Device is Unhealthy \n*Storage Size* : {storage_usage} \n*Message* : Terjadi Kenaikan Storage Melebihi 75% \n*Timestamp* : {time}"
                Bot.notifications(send_alert, "Honeypot Resource Alert")  
                
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
        Collector.add_history_health()

if __name__ == '__main__':
    Main.run()