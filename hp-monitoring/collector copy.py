import random
import paho.mqtt.client as mqtt
import psycopg2
import json
import time
import threading
import telebot
import os
import ping3
import paramiko
from datetime import datetime
from dotenv import load_dotenv


class Connect:
    load_dotenv()

    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt.Client(os.getenv('MQTT_CLIENT_SUBSCRIBE'))
        client.on_connect = on_connect
        client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')))
        return client
    
    def check_ping():
        try:
            while True:
                Collector.cursor.execute("SELECT ip_address, ip_gateway FROM sensors")
                row = Collector.cursor.fetchall()

                for ip in row:
                    ip_address = ip[0]
                    ip_gateway = ip[1]
                    response_address_time = ping3.ping(ip_address, timeout=5)

                    if response_address_time is None:
                        response_gateway_time = ping3.ping(ip_gateway, timeout=5)

                        if response_gateway_time is not None:
                            #kalau Gateway sukses, IP Address mati berarti sensor mati.
                            print(f"Ping to IP Gateway {ip_gateway} successful. Response time: {response_gateway_time} ms")
                            message = f"Sensor : {ip_address} \nCode : 500 \nDescription : Sensor Off \nStatus Honeypot : Off \nat {datetime.now()} \nMessage : Tidak berhasil melakukan update pada perangkat dengan alamat IP {ip_address}. Cek apakah perangkat hidup."
                            return message
                        
                        else:
                            #kalau Gateway gak sukses, IP Address sukses berarti internet mati
                            print(f"Ping to IP Gateway {ip_gateway} timed out.")
                            message = f"Sensor : {ip_address} \nCode : 501 \nDescription : Internet Off \nStatus Honeypot : Off \nat {datetime.now()} \nMessage : Tidak berhasil melakukan update pada perangkat dengan alamat IP {ip_address}. Cek apakah internet pada perangkat hidup."
                            return message
                
                time.sleep(300)
                        
        except (Exception) as error:
            print(error)
    

class Collector(Connect):
    connection = psycopg2.connect(user="postgres",
                                password="scipio",
                                host="10.33.102.212",
                                port=54321,
                                database="hp_automation")
    
    cursor = connection.cursor()
    print('Connected to PostgreSQL')

    def subscribe(client: mqtt):     
        def on_message(client, userdata, msg):
            try:
                global logs_json
                global data
                global alert_message
                logs_json = msg.payload.decode()
                data = json.loads(logs_json)
                
                Collector.insert_data_details()
                alert_message = Collector.add_history()
                Regulation.check_honeypot()

            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record into sensor_details / honeypot_details table {}".format(error))

        client.subscribe(os.getenv('MQTT_TOPIC_SUBSCRIBE'))
        client.on_message = on_message

    def insert_data_details():
        ip_address = data['ip_address'][0]
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


    def add_history():
        try:
            ip_address = data['ip_address'][0]
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

                            # send_alert = f"Sensor : {ip_address} \nCode : 400 \nDescription : Honeypot Off \nStatus Honeypot : {honeypot_status} \nat {current_row_timestamp}"
                            # alert_array.append(send_alert)

                            # Regulation.check_honeypot(ip_address, hp)

                        else:
                            honeypot_status = f"{hp.capitalize()} is {current_row_state}"
                            status_code_id = 1
                            array = (current_row_honeypot_sensor_id, 'On', honeypot_status, status_code_id, current_row_timestamp, current_row_rms, datetime.now().isoformat())
                            sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, started_at, resident_memory_size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                            Collector.cursor.execute(sql_insert_query, array)
                            Collector.connection.commit()
                            print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now().isoformat()}")

                            send_alert = f"Sensor : {ip_address} \nCode : 200 \nDescription : Honeypot On\nStatus Honeypot : {honeypot_status} \nat {current_row_timestamp}"
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

                                send_alert = f"Sensor : {ip_address} \nCode : 401 \nDescription : Honeypot Attack \nStatus Honeypot : {honeypot_status} \nat {current_row_timestamp}"
                                alert_array.append(send_alert)

            return alert_array
                
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into history table {}".format(error))


    def delete_data():
        try:
            while True:
                Collector.cursor.execute("SELECT COUNT(*) FROM sensor_details")
                result_sensor_details = Collector.cursor.fetchone()

                if result_sensor_details[0] > 3:
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


class Regulation(Collector):
    #regulasi ketika honeypot mati
    def check_honeypot():
        try:
            ip_address = data['ip_address'][0]
            Collector.cursor.execute("SELECT COUNT(*) FROM history")
            result = Collector.cursor.fetchone()

            if result[0] > 0:
                honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']

                for hp in honeypot:
                    query = f"SELECT h.honeypot_status FROM history h JOIN honeypot_sensor hs ON h.honeypot_sensor_id = hs.id JOIN honeypots hp ON hs.honeypot_id = hp.id JOIN sensors s ON hs.sensor_id = s.id WHERE hp.name = '{hp}' AND s.ip_address = '{ip_address}' ORDER BY h.created_at DESC LIMIT 1;"
                    Collector.cursor.execute(query)
                    row = Collector.cursor.fetchall()

                    if row:
                        status = row[0][0]
                        if status == f'{hp.capitalize()} is Not Running':
                            #cek honeypot apakah sudah ter-deploy
                            Collector.cursor.execute(f"SELECT * FROM honeypot_sensor hs JOIN honeypots h ON hs.honeypot_id = h.id JOIN sensors s ON hs.sensor_id = s.id WHERE h.name = '{hp}' AND s.ip_address = '{ip_address}'")
                            row_deploy = Collector.cursor.fetchall()

                            # SSH ke sensor
                            if row_deploy:
                                print(f"Honeypot {hp} deployed on IP Address {ip_address}")

                                client = paramiko.SSHClient()
                                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                                hostname = ip_address
                                port = 22888
                                username = 'audrey'
                                password = '050501'
                                # private_key_path = '/home/audrey/.ssh/id_rsa'
                                # private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

                                client.connect(hostname, port=port, username=username, password=password)
                                command = ''

                                if hp == 'dionaea':
                                    command = 'sudo -S docker run --rm -it -p 21:21 -p 42:42 -p 69:69/udp -p 80:80 -p 135:135 -p 443:443 -p 445:445 -p 1433:1433 -p 1723:1723 -p 1883:1883 -p 1900:1900/udp -p 3306:3306 -p 5060:5060 -p 5060:5060/udp -p 5061:5061 -p 11211:11211 -v dionaea:/opt/dionaea -d isif/dionaea:dionaea_hp'

                                if hp == 'honeytrap':
                                    command = 'sudo -S bash dockerize.sh && sudo docker run -it -p 2222:2222 -p 8545:8545 -p 5900:5900 -p 25:25 -p 5037:5037 -p 631:631 -p 389:389 -p 6379:6379 -v honeytrap:/home -d honeytrap_test:latest'

                                if hp == 'gridpot':
                                    command = "sudo -S docker run -it -p 102:102 -p 8000:80 -p 161:161 -p 502:502 -d -v gridpot:/gridpot isif/gridpot:gridpot_hp /bin/bash -c 'cd gridpot; gridlabd -D run_realtime=1 --server ./gridpot/gridlabd/3.1/models/IEEE_13_Node_With_Houses.glm; conpot -t gridpot'"

                                if hp == 'cowrie':
                                    command = 'sudo -S docker run -p 22:2222/tcp -p 23:2223/tcp -v cowrie-etc:/cowrie/cowrie-git/etc -v cowrie-var:/cowrie/cowrie-git/var -d --cap-drop=ALL --read-only isif/cowrie:cowrie_hp'

                                if hp == 'elasticpot':
                                    command = "sudo -S docker run -it -p 9200:9200/tcp -v elasticpot:/elasticpot/log -d isif/elasticpot:elasticpot_hp /bin/sh -c 'cd elasticpot; python3 elasticpot.py'"

                                if hp == 'rdpy':
                                    command = "sudo -S docker run -it -p 3389:3389 -v rdpy:/var/log -d isif/rdpy:rdpy_hp /bin/sh -c 'python /rdpy/bin/rdpy-rdphoneypot.py -l 3389 /rdpy/bin/1 >> /var/log/rdpy.log'"

                                sudo_password = '050501'
                                stdin, stdout, stderr = client.exec_command(command)
                                stdin.write(sudo_password + '\n')
                                stdin.flush()

                                stdout_output = stdout.read().decode().strip()
                                stderr_output = stderr.read().decode().strip()

                                # Check if there is any output
                                if stdout_output:
                                    print(f"Standard Output: {stdout_output}")
                                    print(f"{hp} is successfully running now on sensor {ip_address}")

                                if stderr_output:
                                    print(f"Standard Error: {stderr_output}")

                                client.close()

                    else:
                        print(f"Honeypot {hp} not deployed on IP Address {ip_address}")
        
        except (Exception) as error:
            print(error)


class Bot(Collector):
    API_KEY = os.getenv('API_KEY')
    bot = telebot.TeleBot(API_KEY)
    is_update_running = False

    @bot.message_handler(commands=['start'])
    def send_start_message(message):
        Bot.bot.send_message(chat_id=message.chat.id, text=f"Halo, {message.chat.first_name}! Selamat Datang di Monitoring Sensor & Honeypot Bot. \nBot ini digunakan untuk menginformasikan status terbaru pada Sensor dan Honeypot yang terdaftar.")
        
    @bot.message_handler(commands=['update'])
    def send_update_message(message):
        global alert_message

        if not Bot.is_update_running:
            Bot.is_update_running = True
            Bot.bot.send_message(chat_id=message.chat.id, text="Memulai update status terbaru pada Monitoring Sensor & Honeypot... \nKetik /stop untuk memberhentikan update.")
            
            while Bot.is_update_running:
                if 'alert_message' in locals() or 'alert_message' in globals():
                    if len(alert_message) != 0:
                        for status in alert_message:
                            Bot.bot.send_message(chat_id=message.chat.id, text=status)
                            print(f'Sent message to bot telegram on Honeypot running at {datetime.now()}')
                        alert_message = []
                    else:
                        pass

                if Connect.check_ping():
                    Bot.bot.send_message(chat_id=message.chat.id, text=Connect.check_ping())
                    print(f'Sent message to bot telegram on trouble in device at {datetime.now()}')
                    time.sleep(300)

        
    @bot.message_handler(commands=['stop'])
    def send_start_message(message):
        if Bot.is_update_running:
            Bot.is_update_running = False
            Bot.bot.send_message(chat_id=message.chat.id, text="Memberhentikan update status terbaru pada status Monitoring Sensor & Honeypot. \nKetik /update untuk memulai update.")


class Main(Bot):
    def run_mqtt_loop():
        client = Connect.connect_mqtt()
        Collector.subscribe(client)
        client.loop_forever()

    def run_telegram_bot():
        while True:
            try:
                print('Start Polling...')
                Bot.bot.polling(interval=0, timeout=30)
            except Exception as e:
                print("Error : ", e)

    def run():
        continuous_thread = threading.Thread(target=Collector.delete_data)
        continuous_thread.start()

        telegram_thread = threading.Thread(target=Main.run_telegram_bot)
        telegram_thread.start()

        mqtt_thread = threading.Thread(target=Main.run_mqtt_loop)
        mqtt_thread.start()

        ping_thread = threading.Thread(target=Collector.check_ping)
        ping_thread.start()

    
if __name__ == '__main__':
    Main.run()
    # Main.run_mqtt_loop()
    # Regulation.check_honeypot()