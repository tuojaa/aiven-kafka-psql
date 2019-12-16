import socket


class Uploader(object):
    def __init__(self, producer, connection):
        self.producer = producer
        self.connection = connection

        self.hostname = self._get_hostname()
        self.topic = self._get_topic()

    def _get_hostname(self):
        """
        Get unique hostname for this installation. Used to distinquish data from multiple hosts running this script

        :return: unique hostname
        """
        return socket.gethostname()

    def _get_topic(self):
        """
        Get topic name for Kafka
        :return: topic name
        """
        return "metrics"

    def upload_metrics(self):
        """
        Uploads metrics from producer to connection.

        :param producer: MetricProducer instance
        :param connection: Apache Kafka producer
        :return:
        """

        metrics = self.producer.collect_metrics()
        self.connection.send(self.topic, {
            'host': self.hostname,
            'metrics': metrics
        })
