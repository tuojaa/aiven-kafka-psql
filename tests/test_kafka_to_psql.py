import unittest

from kafka_to_psql import message_to_value_lists


class TestKafkaToPSQL(unittest.TestCase):
    def test_message_to_value_lists(self):
        message = {
            "host": "hostname-123",
            "metrics": {
                "test1": {"a": 1, "b": 2, "c": 3},
                "test2": {"d": 5, "e": 6, "f": 8}
            },
            "timestamp": "2019-12-16T23:00:59.795185"
        }

        value_list = message_to_value_lists(message)
        self.assertEqual(value_list, [
            ['2019-12-16T23:00:59.795185', 'hostname-123', 'test1', 'a', 1],
            ['2019-12-16T23:00:59.795185', 'hostname-123', 'test1', 'b', 2],
            ['2019-12-16T23:00:59.795185', 'hostname-123', 'test1', 'c', 3],
            ['2019-12-16T23:00:59.795185', 'hostname-123', 'test2', 'd', 5],
            ['2019-12-16T23:00:59.795185', 'hostname-123', 'test2', 'e', 6],
            ['2019-12-16T23:00:59.795185', 'hostname-123', 'test2', 'f', 8]
        ])
