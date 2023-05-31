import random
import time
import json
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv


broker = '103.59.95.89'
port = 1883
topic = "monitoring_honeypot"
# generate client ID with pub prefix randomly
client_id = "publisher_honeypot"
# username = 'emqx'
# password = 'public'

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


# def publish(client):
#     main()
#     # msg_count = 0
#     while True:
#         time.sleep(1)
#         msg = json.dumps(logs_json)
#         print(msg)
#         result = client.publish(topic, msg)
#         # result: [0, 1]
#         status = result[0]
#         if status == 0:
#             print(f"Send `{msg}` to topic `{topic}`")
#         else:
#             print(f"Failed to send message to topic {topic}")
        # msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_forever()
    # publish(client)


if __name__ == '__main__':
    run()