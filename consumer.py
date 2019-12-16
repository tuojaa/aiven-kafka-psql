import argparse
import logging
import json
import os
import sys

import psycopg2
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from psycopg2._psycopg import parse_dsn

from kafka_to_psql import insert_message_to_psql

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Forward metrics from Kafka to PostgreSQL')
    parser.add_argument('--server', dest='server', action='store',
                        default=None,
                        help='Kafka bootstrap server')
    parser.add_argument('--psql', dest='psql', action='store',
                        default=None,
                        help='PostgreSQL server')
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

    psql_server = args.psql or os.environ.get('PSQL_SERVER', None)
    if(psql_server is None):
        print("No PSQL server address supplied. Please set PSQL_SERVER environment variable or specify with --psql")
        sys.exit(1)

    try:
        connection = KafkaConsumer(
            'metrics',
            bootstrap_servers=[server_address,],
            security_protocol="SSL",
            ssl_cafile=args.ca,
            ssl_certfile=args.cert,
            ssl_keyfile=args.key,
            value_deserializer=lambda m: json.loads(m.decode('ascii'))
        )
    except KafkaError as e:
        print("Could not connect to Kafka: %s" % (e,))
        sys.exit(1)

    try:
        psql = psycopg2.connect(psql_server)
    except psycopg2.Error as e:
        print("Could not connect to PostgreSQL: %s" % (e,))
        sys.exit(1)

    try:
        for a in connection:
            message = a.value
            try:
                insert_message_to_psql(psql, message)
            except psycopg2.Error as e:
                print("PostgreSQL error: %s" % (e,))
                sys.exit(1)

    except KafkaError as e:
        print("Error in Kafka: %s" % (e,))
        sys.exit(1)
