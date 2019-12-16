import unittest
from datetime import datetime, timedelta

from impl.producer import MetricProducer
from impl.uploader import Uploader


class TestUploader(unittest.TestCase):
    def test_get_hostname(self):
        u = Uploader(None, None)
        self.assertTrue(type(u.hostname), str)
        self.assertGreater(len(u.hostname), 0)
        self.assertNotEqual(u.hostname, "localhost")

    def test_get_topic(self):
        u = Uploader(None, None)
        self.assertTrue(type(u.topic), str)
        self.assertGreater(len(u.topic), 0)

    def test_upload(self):
        class MockConnection(object):
            def __init__(self):
                self.topic = None
                self.data = None

            def send(self, topic, data):
                self.topic = topic
                self.data = data

        mock_metric_data = {'a': 1, 'b': 2}

        class MockProducer(MetricProducer):
            METRICS = {
                "test": lambda: mock_metric_data
            }

        conn = MockConnection()
        p = MockProducer()
        u = Uploader(p, conn)

        self.assertIsNone(conn.topic)
        self.assertIsNone(conn.data)

        u.upload_metrics()

        self.assertIsNotNone(conn.topic)
        self.assertIsNotNone(conn.data)

        self.assertEqual(conn.topic, u.topic)
        self.assertEqual(conn.data['host'], u.hostname)
        self.assertEqual(conn.data['metrics'], {"test": mock_metric_data})
        self.assertIn('timestamp', conn.data)
        self.assertTrue(type(conn.data['timestamp']), str)
        timestamp = datetime.strptime(conn.data['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
        self.assertTrue(datetime.now() - timestamp < timedelta(minutes=1))
