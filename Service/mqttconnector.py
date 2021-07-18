import random
import time
import psycopg2
import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from paho.mqtt import client as mqtt_client

broker = '81.29.139.80'
port = 14883
username = 'emqx'
password = 'public'

class mqttClient(mqtt_client.Client):

    db_client = None

    def test(self):
        pass


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # generate client ID with pub prefix randomly
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqttClient(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, topic):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def start_publish(topic):
    client = connect_mqtt()
    client.loop_start()
    publish(client, topic)


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = msg.payload.decode('UTF-8')
        data = float(data)
        query = 'INSERT INTO public."graps_iotdata"("datetime", "device", "value") VALUES (\'{}\', \'{}\', \'{}\');'.format(datetime.datetime.now().isoformat(), msg.topic, data)
        print(query)
        client.db_client.execute(query)

    client.subscribe(topic)
    client.on_message = on_message
    conn = psycopg2.connect(dbname='PythonIOT', user='postgres', password='P@ssw0rd', host='pgiot')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    client.db_client = conn.cursor()

def start_subscribe(topic):
    client = connect_mqtt()
    subscribe(client, topic)
    client.loop_forever()