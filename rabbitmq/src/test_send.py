#!/usr/bin/env python
import sys, time, threading, perftest

import pika

message_size = 256

if(len(sys.argv) == 2):
    message_size = int(sys.argv[1])

credentials = pika.PlainCredentials('guest', 'guest')
parameters =  pika.ConnectionParameters('192.168.0.170', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange="test_exchange", exchange_type="direct",
                         passive=False, durable=True, auto_delete=False)


producer = perftest.PerfProducer(channel, message_size)
producer.start()

for i in range(1, 50):
    time.sleep(10)
    print "producer sent ", producer.rate.printRate()

producer.stop()

connection.close()
