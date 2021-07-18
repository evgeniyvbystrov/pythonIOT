# python 3.6

import mqttconnector
import threading
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

def db_check():
    try:
        conn = psycopg2.connect(dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PASS'), host=os.environ.get('DB_HOST'))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        db_client = conn.cursor()
        query = 'SELECT * FROM public."graps_iotdata" limit 1;'
        db_client.execute(query)
        print('Connection successful')
        return True

    except:
        print('Waiting for connection')
        return False

class PublishingThread(threading.Thread):

    def __init__(self, topic):
        self.topic = topic
        super().__init__(name="topic" + topic)


    def run(self):
        mqttconnector.start_publish(self.topic)
        print("Thread ", self.topic)

class SubscirbingThread(threading.Thread):

    def __init__(self, topic):
        self.topic = topic
        super().__init__(name="topic" + topic)


    def run(self):
        mqttconnector.start_subscribe(self.topic)
        print("Thread ", self.topic)

if __name__ == '__main__':

    while not db_check():
        time.sleep(1)
#    thread1 = PublishingThread("temperature1")
#    thread1.start()
    thread2 = SubscirbingThread("home/temperature")
    thread2.start()
    thread3 = SubscirbingThread("home/humidity")
    thread3.start()