import logging



# from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers=['localhost:8097', 'localhost:8098', 'localhost:8099'], retries=5)


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    logging.error('I am an errback')


while True:
    print('Input your message: ')
    msg = input()
    producer.send('test_topic', bytes(msg, 'utf-8')).add_callback(on_send_success).add_errback(on_send_error)
    producer.flush()
