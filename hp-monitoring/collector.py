import random
import paho.mqtt.client as mqtt
import psycopg2
import json
import schedule

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

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(config_dict['MQTT_BROKER'], config_dict['MQTT_PORT'])
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        try:
            connection = psycopg2.connect(user="postgres",
                                        password="scipio",
                                        host="10.33.102.212",
                                        port=54321,
                                        database="hp_automation")
            
            cursor = connection.cursor()

            print('Connected to PostgreSQL')

            print(msg.payload.decode())

            # if client.subscribe(topic_sensor):
            #     logs_json = msg.payload.decode()

            #     data = json.loads(logs_json)
            #     array = (1, data['hostname'], data['honeypot_running'], data['CPU_usage'], data['CPU_frequency'], data['CPU_count'], data['RAM_total'], data['RAM_usage'], data['RAM_available'], data['RAM_percentage'], data['swap_memory_total'], data['swap_memory_usage'], data['swap_memory_free'], data['swap_memory_percentage'], data['network_packet_recv'], data['network_packet_sent'], data['datetime'], True)
                
            #     sql_insert_query = """ INSERT INTO sensor_details (sensor_id, sensor_name, honeypot_running, cpu_usage, cpu_frequency, cpu_count, ram_total, ram_usage, ram_available, ram_percentage, swap_memory_total, swap_memory_usage, swap_memory_free, swap_memory_percentage, network_packet_received, network_packet_sent, created_at, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
            #     sql_delete_query = """ DELETE FROM sensor_details WHERE created_at IN (SELECT created_at FROM (SELECT created_at FROM sensor_details ORDER BY created_at ASC LIMIT 1) as Subquery) """


            #     cursor.execute(sql_insert_query, array)
            #     connection.commit()
            #     print(cursor.rowcount, "Record inserted successfully into sensor_details table")

            #     cursor.execute(sql_delete_query)
            #     connection.commit()
            #     print(cursor.rowcount, "Record deleted successfully into sensor_details table")

            # else :
            #     logs_json = msg.payload.decode()

            #     data = json.loads(logs_json)
            #     array = [(1, data['hostname'], 'dionaea', data['dionaea_state'], data['dionaea_virtual_memory'], data['dionaea_resident_memory'], data['dionaea_text_memory'], data['dionaea_data_memory'], data['dionaea_vms_percentage'], data['dionaea_rms_percentage'], data['datetime']),
            #             (2, data['hostname'], 'honeytrap', data['honeytrap_state'], data['honeytrap_virtual_memory'], data['honeytrap_resident_memory'], data['honeytrap_text_memory'], data['honeytrap_data_memory'], data['honeytrap_vms_percentage'], data['honeytrap_rms_percentage'], data['datetime']),
            #             (3, data['hostname'], 'gridpot', data['gridpot_state'], data['gridpot_virtual_memory'], data['gridpot_resident_memory'], data['gridpot_text_memory'], data['gridpot_data_memory'], data['gridpot_vms_percentage'], data['gridpot_rms_percentage'], data['datetime']),
            #             (4, data['hostname'], 'cowrie', data['cowrie_state'], data['cowrie_virtual_memory'], data['cowrie_resident_memory'], data['cowrie_text_memory'], data['cowrie_data_memory'], data['cowrie_vms_percentage'], data['cowrie_rms_percentage'], data['datetime']),
            #             (5, data['hostname'], 'elasticpot', data['elasticpot_state'], data['elasticpot_virtual_memory'], data['elasticpot_resident_memory'], data['elasticpot_text_memory'], data['elasticpot_data_memory'], data['elasticpot_vms_percentage'], data['elasticpot_rms_percentage'], data['datetime']),
            #             (6, data['hostname'], 'rdpy', data['rdpy_state'], data['rdpy_virtual_memory'], data['rdpy_resident_memory'], data['rdpy_text_memory'], data['rdpy_data_memory'], data['rdpy_vms_percentage'], data['rdpy_rms_percentage'], data['datetime']),
            #             ]
                
            #     sql_insert_query = """ INSERT INTO honeypot_details (honeypot_sensor_id, sensor_name, honeypot_name, state, virtual_memory, resident_memory, text_memory, data_memory, virtual_memory_percentage, resident_memory_percentage, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                
            #     cursor.executemany(sql_insert_query, array)
            #     connection.commit()
            #     print(cursor.rowcount, "Record inserted successfully into honeypot_details table")

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

    client.subscribe(topic_sensor)
    client.subscribe(topic_honeypot)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    subscribe(client)

if __name__ == '__main__':
    run()