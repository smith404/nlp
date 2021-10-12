from confluent_kafka import Consumer
from confluent_kafka import KafkaException
from confluent_kafka import KafkaError

conf = {'bootstrap.servers': 'localhost:9092',
        'group.id': "foo",
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}

consumer = Consumer(conf)

running = True

def msg_process(msg):
    print("Got message @" + str(msg.timestamp()))
    print("Offset: " + str(msg.offset()))
    print("Key: " + str(msg.key()))
    print("Value: " + str(msg.value()))


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

basic_consume_loop(consumer, ["sample"])

