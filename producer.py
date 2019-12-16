from metrics import get_cpu_usage


class MetricProducer(object):

    def collect_metrics(self):
        """
        Collect metrics. Each metric will be a dictionary, containing submetrics as key-value pairs

        :return: Dictionary of dictionaries
        """
        return {
            'cpu': get_cpu_usage()
        }
