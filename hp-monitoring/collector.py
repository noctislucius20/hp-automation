import random
import paho.mqtt.client as mqtt
import psycopg2
import json

client_id = f'python-mqtt-{random.randint(0, 100)}'
config_file = open('hp-monitoring/config.txt')
config_dict = {}
for lines in config_file:
    items = lines.split(': ', 1)
    config_dict[items[0]] = eval(items[1])

topic = 'topic/monitoring/#'

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
        logs_json = msg.payload.decode()
        array = []

        data = json.loads(logs_json)
        array = [(1, data['hostname'], 'dionaea', data['dionaea_state'], data['dionaea_virtual_memory'], data['dionaea_resident_memory'], data['dionaea_text_memory'], data['dionaea_data_memory'], data['dionaea_vms_percentage'], data['dionaea_rms_percentage'], data['datetime']),
                 (2, data['hostname'], 'honeytrap', data['honeytrap_state'], data['honeytrap_virtual_memory'], data['honeytrap_resident_memory'], data['honeytrap_text_memory'], data['honeytrap_data_memory'], data['honeytrap_vms_percentage'], data['honeytrap_rms_percentage'], data['datetime']),
                 (3, data['hostname'], 'gridpot', data['gridpot_state'], data['gridpot_virtual_memory'], data['gridpot_resident_memory'], data['gridpot_text_memory'], data['gridpot_data_memory'], data['gridpot_vms_percentage'], data['gridpot_rms_percentage'], data['datetime']),
                 (4, data['hostname'], 'cowrie', data['cowrie_state'], data['cowrie_virtual_memory'], data['cowrie_resident_memory'], data['cowrie_text_memory'], data['cowrie_data_memory'], data['cowrie_vms_percentage'], data['cowrie_rms_percentage'], data['datetime']),
                 (5, data['hostname'], 'elasticpot', data['elasticpot_state'], data['elasticpot_virtual_memory'], data['elasticpot_resident_memory'], data['elasticpot_text_memory'], data['elasticpot_data_memory'], data['elasticpot_vms_percentage'], data['elasticpot_rms_percentage'], data['datetime']),
                 (6, data['hostname'], 'rdpy', data['rdpy_state'], data['rdpy_virtual_memory'], data['rdpy_resident_memory'], data['rdpy_text_memory'], data['rdpy_data_memory'], data['rdpy_vms_percentage'], data['rdpy_rms_percentage'], data['datetime']),
                ]

        print(f"Received `{array}` from `{msg.topic}` topic")

        try:
            connection = psycopg2.connect(user="postgres",
                                        password="scipio",
                                        host="10.33.102.212",
                                        port=54321,
                                        database="hp_automation")
            
            cursor = connection.cursor()

            print('Connected to PostgreSQL')

            sql_insert_query = """ INSERT INTO honeypot_details (honeypot_sensor_id, sensor_name, honeypot_name, state, virtual_memory, resident_memory, text_memory, data_memory, virtual_memory_percentage, resident_memory_percentage, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
            
            result = cursor.executemany(sql_insert_query, array)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into honeypot_details table")

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into honeypot_details table {}".format(error))

        # finally:
        #     if connection:
        #         cursor.close()
        #         connection.close()
        #         print("PostgreSQL connection is closed")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    subscribe(client)

if __name__ == '__main__':
    run()