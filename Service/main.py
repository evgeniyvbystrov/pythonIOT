# python 3.6

import mqttconnector
import threading


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

#    thread1 = PublishingThread("temperature1")
#    thread1.start()
    thread2 = SubscirbingThread("home/temperature")
    thread2.start()
    thread3 = SubscirbingThread("home/humidity")
    thread3.start()