import argparse
import logging
import json
import os
import sys
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError

from producer import MetricProducer
from uploader import Uploader

logger = logging.getLogger(__name__)

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Upload system metrics to Apache Kafka')
    parser.add_argument('--server', dest='server', action='store',
                        default=None,
                        help='Kafka bootstrap server')
    parser.add_argument('--ca', dest='ca', action='store',
                        default="ca.pem",
                        help='Kafka CA file')
    parser.add_argument('--cert', dest='cert', action='store',
                        default="service.cert",
                        help='Kafka server certificate file')
    parser.add_argument('--key', dest='key', action='store',
                        default="service.key",
                        help='Kafka server key file')
    parser.add_argument('-v', dest='verbosity', action='count',
                        default=0,
                        help="Verbosity")
    args = parser.parse_args()

    loglevel = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.INFO,
        3: logging.DEBUG
    }[args.verbosity]

    logging.basicConfig(format='%(levelname)s:%(message)s', level=loglevel)

    server_address = args.server or os.environ.get('KAFKA_SERVER', None)

    if(server_address is None):
        print("No Kafka server address supplied. Please set KAFKA_SERVER environment variable or specify with --server")
        sys.exit(1)

    producer = MetricProducer()
    try:
        connection = KafkaProducer(
            bootstrap_servers=[server_address,],
            security_protocol="SSL",
            ssl_cafile=args.ca,
            ssl_certfile=args.cert,
            ssl_keyfile=args.key,
            value_serializer=lambda m: json.dumps(m).encode('ascii')
        )
    except KafkaError as e:
        print("Could not connect to Kafka: %s" % (e,))
        sys.exit(1)

    u = Uploader(producer, connection)
    print("Ready to produce metrics, stop by pressing CTRL-C")
    while(True):
        try:
            u.upload_metrics()
        except KafkaError as e:
            print("Error in Kafka: %s" % (e,))
            sys.exit(1)

        logger.info("Metrics uploaded")
        time.sleep(1)
