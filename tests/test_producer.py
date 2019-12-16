import unittest

from producer import MetricProducer


class TestProducer(unittest.TestCase):

    def test_collect_metrics(self):
        p = MetricProducer()

        metrics = p.collect_metrics()

        self.assertTrue(type(metrics) is dict)
        self.assertIn('cpu', metrics)
