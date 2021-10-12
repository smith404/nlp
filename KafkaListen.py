import sys, getopt

from confluent_kafka import Consumer
from confluent_kafka import KafkaException
from confluent_kafka import KafkaError

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

def main(argv):
    groupId = 'foo'

    try:
        opts, args = getopt.getopt(argv,"hg:",["group_id="])
    except getopt.GetoptError:
        print('KafkaListen.py -g <group id>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('KafkaListen.py -g <group id>')
            sys.exit()
        elif opt in ("-g", "--group_id"):
            groupId = arg

    conf = {'bootstrap.servers': 'localhost:9092',
            'group.id': groupId,
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest'}

    consumer = Consumer(conf)

    basic_consume_loop(consumer, ["sample"])

running = True

if __name__ == "__main__":
   main(sys.argv[1:])
