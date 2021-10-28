from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)

producer.produce('sample', b'Hello, World!')
producer.produce('sample', key=b'message-two', value=b'This is Kafka-Python')
producer.flush()