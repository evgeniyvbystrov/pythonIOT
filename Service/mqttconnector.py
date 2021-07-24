import random
import time
import psycopg2
import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from paho.mqtt import client as mqtt_client

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
    client.username_pw_set(os.environ.get('MQTT_LOGIN'), os.environ.get('MQTT_PASS'))
    client.on_connect = on_connect
    broker = os.environ.get('MQTT_IP')
    port = int(os.environ.get('MQTT_PORT'))
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(10)
        query = 'SELECT device, task FROM public.graps_tasks WHERE ' \
                '(device, id) IN (SELECT device, MAX(id) FROM public.graps_tasks GROUP BY device)'
        client.db_client.execute(query)
        for r in client.db_client:
            topic = r[0] + '/tasks'
            msg = str(r[1])
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Sent `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
        msg_count += 1


def start_publish():
    client = connect_mqtt()
    client.loop_start()
    conn = psycopg2.connect(dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'), host=os.environ.get('DB_HOST'))
    client.db_client = conn.cursor()
    publish(client)


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = msg.payload.decode('UTF-8')
        data = float(data)
        query = 'INSERT INTO public."graps_iotdata"("datetime", "device", "value") VALUES (\'{}\', \'{}\', \'{}\');'.format(datetime.datetime.now().isoformat(), msg.topic, data)
        #print(query)
        client.db_client.execute(query)

    client.subscribe(topic)
    client.on_message = on_message
    conn = psycopg2.connect(dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'), host=os.environ.get('DB_HOST'))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    client.db_client = conn.cursor()


def start_subscribe(topic):
    client = connect_mqtt()
    subscribe(client, topic)
    client.loop_forever()