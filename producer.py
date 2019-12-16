from metrics import get_cpu_usage, get_memory_usage


class MetricProducer(object):
    METRICS = {
        "cpu": get_cpu_usage,
        "mem": get_memory_usage
    }

    def collect_metrics(self):
        """
        Collect metrics. Each metric will be a dictionary, containing submetrics as key-value pairs

        :return: Dictionary of dictionaries
        """
        return {
            key: value() for key, value in self.METRICS.items()
        }
