import random
import paho.mqtt.client as mqtt
import psycopg2
import json
import time
import threading
from datetime import datetime
import telebot
from dotenv import load_dotenv


class Connect:
    client_id = f'python-mqtt-{random.randint(0, 100)}'
    config_file = open('hp-monitoring/config.txt')
    config_dict = {}
    for lines in config_file:
        items = lines.split(': ', 1)
        config_dict[items[0]] = eval(items[1])

    topic = 'topic/monitoring/#'
    # topic_sensor = 'topic/monitoring/sensor/+'
    # topic_honeypot = 'topic/monitoring/honeypot/+'

    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt.Client(Connect.client_id)
        client.on_connect = on_connect
        client.connect(Connect.config_dict['MQTT_BROKER'], Connect.config_dict['MQTT_PORT'])
        return client


class Collector(Connect):
    connection = psycopg2.connect(user="postgres",
                                password="scipio",
                                host="10.33.102.212",
                                port=54321,
                                database="hp_automation")
    
    cursor = connection.cursor()
    print('Connected to PostgreSQL')


    def get_chat_id(chat_id):
        global message_chat_id
        message_chat_id = chat_id

    def subscribe(client: mqtt):     
        def on_message(client, userdata, msg):
            try:
                global logs_json
                global data
                global alert_message
                logs_json = msg.payload.decode()
                data = json.loads(logs_json)
                
                Collector.insert_data_details()
                alert_message = Collector.add_history(1)

            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record into sensor_details / honeypot_details table {}".format(error))

            # finally:
            #     if connection:
            #         if client.subscribe(topic_sensor):
            #             sql_delete_query = """ DELETE FROM sensor_details WHERE created_at IN (SELECT created_at FROM (SELECT created_at FROM sensor_details ORDER BY created_at ASC LIMIT 1) as Subquery) """
            #             cursor.execute(sql_delete_query)
            #             print(cursor.rowcount, "Record deleted successfully into sensor_details table")

                    # cursor.close()
                    # connection.close()
                    # print("PostgreSQL connection is closed")

        client.subscribe(Connect.topic)
        client.on_message = on_message

    def insert_data_details():
        ip_address = data['ip_address'][1]
        id_sensor = 0

        if "id_raspi" in data:
            Collector.cursor.execute(f"SELECT id FROM sensors WHERE ip_address = '{ip_address}'")
            row = Collector.cursor.fetchone()

            if row:
                id_sensor = row[0]
            else:
                id_sensor = 1

            array = (id_sensor, data['hostname'], data['honeypot_running'], data['CPU_usage'], data['CPU_frequency'], data['CPU_count'], data['RAM_total'], data['RAM_usage'], data['RAM_available'], data['RAM_percentage'], data['swap_memory_total'], data['swap_memory_usage'], data['swap_memory_free'], data['swap_memory_percentage'], data['network_packet_recv'], data['network_packet_sent'], data['datetime'], True)
            sql_insert_query = """ INSERT INTO sensor_details (sensor_id, sensor_name, honeypot_running, cpu_usage, cpu_frequency, cpu_count, ram_total, ram_usage, ram_available, ram_percentage, swap_memory_total, swap_memory_usage, swap_memory_free, swap_memory_percentage, network_packet_received, network_packet_sent, created_at, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

            Collector.cursor.execute(sql_insert_query, array)
            Collector.connection.commit()
            print(Collector.cursor.rowcount, f"Record inserted successfully into sensor_details table : {datetime.now().isoformat()}")

        if "id_honeypot" in data :
            honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
            get_id_honeypot_sensor = []
            array_query = []

            for index, value in enumerate(honeypot):
                Collector.cursor.execute(f"SELECT hs.id FROM honeypot_sensor hs JOIN honeypots h ON hs.honeypot_id = h.id JOIN sensors s ON hs.sensor_id = s.id WHERE h.name = '{value}' AND s.ip_address = '{ip_address}'")
                row = Collector.cursor.fetchall()

                if row:
                    id = row[0][0]
                else:
                    id = int(index) + 1

                get_id_honeypot_sensor.append(id)

            for id_honeypot_sensor, honeypot_name in zip(get_id_honeypot_sensor, honeypot):
                query = (id_honeypot_sensor, data['hostname'], honeypot_name, data[f'{honeypot_name}_state'], data[f'{honeypot_name}_virtual_memory'], data[f'{honeypot_name}_resident_memory'], data[f'{honeypot_name}_text_memory'], data[f'{honeypot_name}_data_memory'], data[f'{honeypot_name}_vms_percentage'], data[f'{honeypot_name}_rms_percentage'], data['datetime'])
                array_query.append(query)  
            
            sql_insert_query = """ INSERT INTO honeypot_details (honeypot_sensor_id, sensor_name, honeypot_name, state, virtual_memory, resident_memory, text_memory, data_memory, virtual_memory_percentage, resident_memory_percentage, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
            
            Collector.cursor.executemany(sql_insert_query, array_query)
            Collector.connection.commit()
            print(Collector.cursor.rowcount, f"Record inserted successfully into honeypot_details table : {datetime.now().isoformat()}")


    def add_history(data_logs):
        try:
            ip_address = data['ip_address'][1]
            Collector.cursor.execute("SELECT COUNT(*) FROM honeypot_details")
            result = Collector.cursor.fetchone()
            global alert_array

            if result[0] > 0:
                honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
                
                array = []
                alert_array = []

                for hp in honeypot:
                    query = f"SELECT honeypot_sensor_id, state, resident_memory, created_at FROM honeypot_details WHERE honeypot_sensor_id IN (SELECT honeypot_sensor.id FROM honeypot_sensor JOIN honeypots ON honeypots.id = honeypot_sensor.honeypot_id JOIN sensors ON sensors.id = honeypot_sensor.sensor_id WHERE sensors.ip_address = '{ip_address}') AND honeypot_name = '{hp}' ORDER BY created_at DESC LIMIT 2;"
                    Collector.cursor.execute(query)
                    row = Collector.cursor.fetchall()
                
                    if len(row) < 1:
                        current_row_honeypot_sensor_id = None
                        current_row_state = None
                        current_row_rms = None
                        current_row_timestamp = None
                    else:
                        current_row_honeypot_sensor_id = row[0][0]
                        current_row_state = row[0][1]
                        current_row_rms = row[0][2]
                        current_row_timestamp = row[0][3]
                    
                    late_row_state = None if len(row) < 2 else row[1][1]
                    late_row_rms = None if len(row) < 2 else row[1][2]

                    if current_row_state != late_row_state:
                        if current_row_state == 'Not Running':
                            honeypot_status = f"{hp.capitalize()} is {current_row_state}"
                            status_code_id = 2
                            array = (current_row_honeypot_sensor_id, 'On', honeypot_status, status_code_id, current_row_timestamp, current_row_rms, datetime.now().isoformat())
                            sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                            Collector.cursor.execute(sql_insert_query, array)
                            Collector.connection.commit()
                            print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now().isoformat()}")

                            send_alert = f"Sensor : {ip_address} \nCode : 400 \nDescription: Honeypot Off \nStatus Honeypot : {honeypot_status} \nat {current_row_timestamp}"
                            alert_array.append(send_alert)

                        else:
                            honeypot_status = f"{hp.capitalize()} is {current_row_state}"
                            status_code_id = 1
                            array = (current_row_honeypot_sensor_id, 'On', honeypot_status, status_code_id, current_row_timestamp, current_row_rms, datetime.now().isoformat())
                            sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, started_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                            Collector.cursor.execute(sql_insert_query, array)
                            Collector.connection.commit()
                            print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now().isoformat()}")

                            send_alert = f"Sensor : {ip_address} \nCode : 200 \nDescription: Honeypot On\nStatus Honeypot : {honeypot_status} \nat {current_row_timestamp}"
                            alert_array.append(send_alert)

                    else:
                        if current_row_rms is not None and late_row_rms is not None:
                            if current_row_rms > late_row_rms:
                                honeypot_status = f"There is attack on honeypot {hp.capitalize()}"
                                status_code_id = 4
                                array = (current_row_honeypot_sensor_id, 'On', honeypot_status, status_code_id, current_row_timestamp, current_row_rms, datetime.now().isoformat())
                                sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, threat_activity_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                                Collector.cursor.execute(sql_insert_query, array)
                                Collector.connection.commit()
                                print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now().isoformat()}")

                                send_alert = f"Sensor : {ip_address} \nCode : 401 \nDescription: Honeypot Attack \nStatus Honeypot : {honeypot_status} \nat {current_row_timestamp}"
                                alert_array.append(send_alert)

            return alert_array
                
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into history table {}".format(error))


    def delete_data():
        try:
            while True:
                Collector.cursor.execute("SELECT COUNT(*) FROM sensor_details")
                result_sensor_details = Collector.cursor.fetchone()

                if result_sensor_details[0] > 5:
                    sql_delete_query_sensor_details = """ DELETE FROM sensor_details WHERE created_at IN (SELECT created_at FROM (SELECT created_at FROM sensor_details ORDER BY created_at ASC LIMIT 1) as Subquery) """

                    Collector.cursor.execute(sql_delete_query_sensor_details)
                    Collector.connection.commit()
                    print(Collector.cursor.rowcount, "Record deleted successfully into sensor_details table")
                
                Collector.cursor.execute("SELECT COUNT(*) FROM honeypot_details")
                result_honeypot_details = Collector.cursor.fetchone()

                if result_honeypot_details[0] > 17:
                    sql_delete_query_honeypot_details = """ DELETE FROM honeypot_details WHERE created_at IN (SELECT created_at FROM (SELECT created_at FROM honeypot_details ORDER BY created_at ASC LIMIT 6) as Subquery) """

                    Collector.cursor.execute(sql_delete_query_honeypot_details)
                    Collector.connection.commit()
                    print(Collector.cursor.rowcount, "Record deleted successfully into honeypot_details table")
                
                time.sleep(30)     

        except (Exception, psycopg2.Error) as error:
            print("Failed to delete record into sensor_details / honeypot_details table {}".format(error))
            row = Collector.cursor.fetchone()
            print(row)


class Bot(Collector):
    API_KEY = '6289233331:AAG_l-CfrztpTtYs_9o6ZtKo2adniEi8_Ig'
    bot = telebot.TeleBot(API_KEY)
    is_update_running = False

    @bot.message_handler(commands=['start'])
    def send_start_message(message, self):
        Bot.bot.send_message(chat_id=message.chat.id, text=f"Halo, {message.chat.first_name}! Selamat Datang di Monitoring Sensor & Honeypot Bot. \nBot ini digunakan untuk menginformasikan status terbaru pada Sensor dan Honeypot yang terdaftar.")
        
    @bot.message_handler(commands=['update'])
    def send_update_message(message):
        global alert_message

        if not Bot.is_update_running:
            Bot.is_update_running = True
            Bot.bot.send_message(chat_id=message.chat.id, text="Melakukan update status terbaru pada Monitoring Sensor & Honeypot... \nKetik /stop untuk memberhentikan update.")
            
            while Bot.is_update_running:
                if 'alert_message' in locals() or 'alert_message' in globals():
                    if len(alert_message) != 0:
                        for status in alert_message:
                            Bot.bot.send_message(chat_id=message.chat.id, text=status)
                            print(f'Sent message to bot telegram at {datetime.now()}')
                        alert_message = []
                    else:
                        pass

        
    @bot.message_handler(commands=['stop'])
    def send_start_message(message):
        if Bot.is_update_running:
            Bot.is_update_running = False
            Bot.bot.send_message(chat_id=message.chat.id, text="Memberhentikan notifikasi update pada status Honeypot.")

        
class Main(Bot):
    def run_mqtt_loop():
        client = Connect.connect_mqtt()
        Collector.subscribe(client)
        client.loop_forever()

    def run_telegram_bot():
        while True:
            try:
                print('Start Polling...')
                Bot.bot.polling()
            except Exception as e:
                print("Error : ", e)

    def run():
        continuous_thread = threading.Thread(target=Collector.delete_data)
        continuous_thread.start()

        telegram_thread = threading.Thread(target=Main.run_telegram_bot)
        telegram_thread.start()

        mqtt_thread = threading.Thread(target=Main.run_mqtt_loop)
        mqtt_thread.start()

    
if __name__ == '__main__':
    Main.run()