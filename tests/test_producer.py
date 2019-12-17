import unittest

from aiven_kafka_psql.impl.producer import MetricProducer


class TestProducer(unittest.TestCase):

    def test_collect_metrics(self):
        p = MetricProducer()

        metrics = p.collect_metrics()

        self.assertTrue(type(metrics) is dict)
        self.assertIn('cpu', metrics)
        self.assertTrue(type(metrics['cpu']) is dict)
        self.assertIn('mem', metrics)
        self.assertTrue(type(metrics['mem']) is dict)
