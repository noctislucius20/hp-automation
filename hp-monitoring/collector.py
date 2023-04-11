import random
import paho.mqtt.client as mqtt
import psycopg2
import json
import schedule
import time

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
    
    def subscribe(client: mqtt):     
        def on_message(client, userdata, msg):
            try:           
                cursor = Collector.connection.cursor()
                print('Connected to PostgreSQL')

                logs_json = msg.payload.decode()
                data = json.loads(logs_json)

                if "CPU_usage" in data:
                    ip_address = data['ip_address']
                    ip_addr = ''
                    id_sensor = 0
                    
                    if ip_address[0].find('en') != -1 or ip_address[0].find('eth') != -1:
                        ip_addr = str(data['ip_address'][1])
                    else:
                        ip_addr = str(0)

                    cursor.execute(f"SELECT id FROM sensors WHERE ip_address = '{ip_addr}'")
                    row = cursor.fetchone()

                    if row:
                        id_sensor = row[0]
                    else:
                        id_sensor = 1

                    array = (id_sensor, data['hostname'], data['honeypot_running'], data['CPU_usage'], data['CPU_frequency'], data['CPU_count'], data['RAM_total'], data['RAM_usage'], data['RAM_available'], data['RAM_percentage'], data['swap_memory_total'], data['swap_memory_usage'], data['swap_memory_free'], data['swap_memory_percentage'], data['network_packet_recv'], data['network_packet_sent'], data['datetime'], True)
                    sql_insert_query = """ INSERT INTO sensor_details (sensor_id, sensor_name, honeypot_running, cpu_usage, cpu_frequency, cpu_count, ram_total, ram_usage, ram_available, ram_percentage, swap_memory_total, swap_memory_usage, swap_memory_free, swap_memory_percentage, network_packet_received, network_packet_sent, created_at, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

                    cursor.execute(sql_insert_query, array)
                    Collector.connection.commit()
                    print(cursor.rowcount, "Record inserted successfully into sensor_details table")

                else :
                    array = [(1, data['hostname'], 'dionaea', data['dionaea_state'], data['dionaea_virtual_memory'], data['dionaea_resident_memory'], data['dionaea_text_memory'], data['dionaea_data_memory'], data['dionaea_vms_percentage'], data['dionaea_rms_percentage'], data['datetime']),
                            (2, data['hostname'], 'honeytrap', data['honeytrap_state'], data['honeytrap_virtual_memory'], data['honeytrap_resident_memory'], data['honeytrap_text_memory'], data['honeytrap_data_memory'], data['honeytrap_vms_percentage'], data['honeytrap_rms_percentage'], data['datetime']),
                            (3, data['hostname'], 'gridpot', data['gridpot_state'], data['gridpot_virtual_memory'], data['gridpot_resident_memory'], data['gridpot_text_memory'], data['gridpot_data_memory'], data['gridpot_vms_percentage'], data['gridpot_rms_percentage'], data['datetime']),
                            (4, data['hostname'], 'cowrie', data['cowrie_state'], data['cowrie_virtual_memory'], data['cowrie_resident_memory'], data['cowrie_text_memory'], data['cowrie_data_memory'], data['cowrie_vms_percentage'], data['cowrie_rms_percentage'], data['datetime']),
                            (5, data['hostname'], 'elasticpot', data['elasticpot_state'], data['elasticpot_virtual_memory'], data['elasticpot_resident_memory'], data['elasticpot_text_memory'], data['elasticpot_data_memory'], data['elasticpot_vms_percentage'], data['elasticpot_rms_percentage'], data['datetime']),
                            (6, data['hostname'], 'rdpy', data['rdpy_state'], data['rdpy_virtual_memory'], data['rdpy_resident_memory'], data['rdpy_text_memory'], data['rdpy_data_memory'], data['rdpy_vms_percentage'], data['rdpy_rms_percentage'], data['datetime']),
                            ]
                    
                    sql_insert_query = """ INSERT INTO honeypot_details (honeypot_sensor_id, sensor_name, honeypot_name, state, virtual_memory, resident_memory, text_memory, data_memory, virtual_memory_percentage, resident_memory_percentage, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                    
                    cursor.executemany(sql_insert_query, array)
                    Collector.connection.commit()
                    print(cursor.rowcount, "Record inserted successfully into honeypot_details table")

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

    def delete_data():
        try:      
            time.sleep(60)     
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

    def run():
        client = Connect.connect_mqtt()
        # Collector.subscribe(client)
        client.loop_start()
        while True:
            Collector.subscribe(client)
            Collector.delete_data()

if __name__ == '__main__':
    Collector.run()

    # schedule.every(1).minute.do(Collector.delete_data)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)