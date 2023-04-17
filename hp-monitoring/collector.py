import random
import paho.mqtt.client as mqtt
import psycopg2
import json
import schedule
import time
import threading
from datetime import datetime

class Connect:
    client_id = f'python-mqtt-{random.randint(0, 100)}'
    config_file = open('hp-monitoring/config.txt')
    config_dict = {}
    for lines in config_file:
        items = lines.split(': ', 1)
        config_dict[items[0]] = eval(items[1])

    topic_sensor = 'topic/monitoring/sensor/+'
    topic_honeypot = 'topic/monitoring/honeypot/+'

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

    def subscribe(client: mqtt):     
        def on_message(client, userdata, msg):
            try:
                global logs_json
                global data          
                logs_json = msg.payload.decode()
                data = json.loads(logs_json)
                 
                Collector.insert_data_details()
                Collector.add_history(data=1)

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

        client.subscribe(Connect.topic_sensor)
        client.subscribe(Connect.topic_honeypot)
        client.on_message = on_message

    def insert_data_details():
        ip_address = data['ip_address']
        ip_addr = ''
        id_sensor = 0
        
        if ip_address[0].find('en') != -1 or ip_address[0].find('eth') != -1:
            ip_addr = str(data['ip_address'][1])
        else:
            ip_addr = str('0.0.0.0')

        if "id_raspi" in data:
            Collector.cursor.execute(f"SELECT id FROM sensors WHERE ip_address = '{ip_addr}'")
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
                Collector.cursor.execute(f"SELECT hs.id FROM honeypot_sensor hs JOIN honeypots h ON hs.honeypot_id = h.id JOIN sensors s ON hs.sensor_id = s.id WHERE h.name = '{value}' AND s.ip_address = '{ip_addr}'")
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


    def add_history(data):
        try:
            #sensor mati
            if data == 0:
                array = [(1, 'off', 'dionaea off', datetime.now().isoformat(), datetime.now().isoformat()),
                        (2, 'off', 'honeytrap off', datetime.now().isoformat(), datetime.now().isoformat()), 
                        (3, 'off', 'gridpot off', datetime.now().isoformat(), datetime.now().isoformat()), 
                        (4, 'off', 'cowrie off', datetime.now().isoformat(), datetime.now().isoformat()), 
                        (5, 'off', 'elasticpot off', datetime.now().isoformat(), datetime.now().isoformat()),
                        (6, 'off', 'rdpy off', datetime.now().isoformat(), datetime.now().isoformat()),
                        ]
                
                sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, stopped_at, created_at) VALUES (%s, %s, %s, %s, %s) """
                            
                Collector.cursor.executemany(sql_insert_query, array)
                Collector.connection.commit()
                print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now().isoformat()}")

            else:
                Collector.cursor.execute("SELECT COUNT(*) FROM honeypot_details")
                result = Collector.cursor.fetchone()

                if result[0] > 0:
                    honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
                    
                    array = []

                    for hp in honeypot:
                        Collector.cursor.execute(f"select honeypot_sensor_id, state, created_at from honeypot_details hd where honeypot_name = '{hp}' order by created_at desc limit 2")
                        row = Collector.cursor.fetchall()
                    
                        if len(row) < 1:
                            current_row_honeypot_sensor_id = None
                            current_row_state = None
                            current_row_timestamp = None
                        else:
                            current_row_honeypot_sensor_id = row[0][0]
                            current_row_state = row[0][1]
                            current_row_timestamp = row[0][2]
                        
                        late_row_state = None if len(row) < 2 else row[1][1]

                        if current_row_state != late_row_state:
                            # if late_row_state == None:
                                if current_row_state == 'Not Running':
                                    honeypot_status = f"{hp.capitalize()} {current_row_state}"
                                    status_code_id = 2
                                    array = (current_row_honeypot_sensor_id, 'On', honeypot_status, status_code_id, current_row_timestamp, datetime.now().isoformat())
                                    sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, stopped_at, created_at) VALUES (%s, %s, %s, %s, %s, %s)"""

                                    Collector.cursor.execute(sql_insert_query, array)
                                    Collector.connection.commit()
                                    print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now().isoformat()}")

                                else:
                                    honeypot_status = f"{hp.capitalize()} {current_row_state}"
                                    status_code_id = 1
                                    array = (current_row_honeypot_sensor_id, 'On', honeypot_status, status_code_id, current_row_timestamp, datetime.now().isoformat())
                                    sql_insert_query = """ INSERT INTO history (honeypot_sensor_id, sensor_status, honeypot_status, status_code_id, started_at, created_at) VALUES (%s, %s, %s, %s, %s, %s)"""

                                    Collector.cursor.execute(sql_insert_query, array)
                                    Collector.connection.commit()
                                    print(Collector.cursor.rowcount, f"Record inserted successfully into history table : {datetime.now().isoformat()}")
        
        except (Exception, psycopg2.Error) as error:
                print("Failed to insert record into history table {}".format(error))


    def delete_data():
        try:      
            # time.sleep(60)     
            cursor = Collector.connection.cursor()
            print('Connected to PostgreSQL')

            sql_delete_query_sensor_details = """ DELETE FROM sensor_details WHERE created_at IN (SELECT created_at FROM (SELECT created_at FROM sensor_details ORDER BY created_at ASC LIMIT 1) as Subquery) """

            cursor.execute(sql_delete_query_sensor_details)
            Collector.connection.commit()
            print(cursor.rowcount, "Record deleted successfully into sensor_details table")

            sql_delete_query_honeypot_details = """ DELETE FROM honeypot_details WHERE created_at IN (SELECT created_at FROM (SELECT created_at FROM honeypot_details ORDER BY created_at ASC LIMIT 6) as Subquery) """

            cursor.execute(sql_delete_query_honeypot_details)
            Collector.connection.commit()
            print(cursor.rowcount, "Record deleted successfully into honeypot_details table")

        except (Exception, psycopg2.Error) as error:
            print("Failed to delete record into sensor_details / honeypot_details table {}".format(error))
            row = Collector.cursor.fetchone()
            print(row)

    def run():
        client = Connect.connect_mqtt()
        # Collector.subscribe(client)
        client.loop_start()
        timeout = 60
        start_time = time.time()
        first_message_received = False
        while True:
            # pass
            # Collector.subscribe(client)
            # Collector.add_history(client)
            # Collector.add_history()
            # Collector.delete_data()

            if time.time() - start_time == timeout:
                Collector.add_history(data=0)
                break
            else:
                data = 1
                Collector.subscribe(client)
                # print(last_message)
                # Collector.add_history(data=1, last_message=last_message)

        client.loop_stop()
        client.disconnect()


if __name__ == '__main__':
    Collector.run()

    # schedule.every(1).minute.do(Collector.delete_data)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)