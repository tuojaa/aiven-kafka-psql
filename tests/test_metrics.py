import unittest

import metrics


class TestMetrics(unittest.TestCase):
    def test_get_cpu_usage(self):
        cpu = metrics.get_cpu_usage()
        self.assertTrue(type(cpu) is dict)

        self.assertIn('user', cpu)
        self.assertIn('system', cpu)
        self.assertIn('idle', cpu)

        self.assertTrue(type(cpu['user']) is float)
        self.assertTrue(type(cpu['system']) is float)
        self.assertTrue(type(cpu['idle']) is float)

        total = cpu['user']+cpu['system']+cpu['idle']
        self.assertAlmostEqual(total, 1.0)
