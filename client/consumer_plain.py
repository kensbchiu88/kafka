from confluent_kafka import Consumer, KafkaException, KafkaError
import avro.schema
import avro.io
import io
import sys

if __name__ == "__main__":

    # To consume messages
    conf = {'bootstrap.servers': 'localhost:9097',
            'group.id': 'my_group',
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_PLAINTEXT',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': 'redpanda',
            'sasl.password': 'redpandasecret12'
            }
    consumer = Consumer(**conf)
    topic = consumer.subscribe(['user'])

    schema_path = "user.avsc"
    schema = avro.schema.Parse(open(schema_path).read())

    try:
        running = True
        while running:
            msg = consumer.poll(timeout=60000)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(),
                                      msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))

            message = msg.value()
            bytes_reader = io.BytesIO(message)
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(schema)
            try:
                decoded_msg = reader.read(decoder)
                print(decoded_msg)
                sys.stdout.flush()
            except AssertionError:
                continue

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')