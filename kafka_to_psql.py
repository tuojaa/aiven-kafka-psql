import datetime

from psycopg2.extras import execute_values


def message_to_value_lists(message):
    """
    Convert Kafka metrics message into value lists for SQL insert many statement

    :param message: Message value as it arrives through Kafka
    :return: list of value lists to be inserted to PostgreSQL
    """

    # pull out common values for all rows
    hostname = message['host']
    metrics = message['metrics']
    timestamp = message['timestamp']

    values = []

    # traverse message structure (double dictionary)
    for metric_key, metric_values in metrics.items():
        for submetric_key, value in metric_values.items():
            # emit values for each row to be inserted to SQL
            values.append([timestamp, hostname, metric_key, submetric_key, value])

    return values

def insert_message_to_psql(conn, message):
    """
    Insert metrics message to PostgreSQL

    :param conn: PostgreSQL Connection
    :param message: Kafka message value
    :return:
    """
    value_list = message_to_value_lists(message)

    cursor = conn.cursor()
    execute_values(
        cursor,
        "INSERT INTO metrics (timestamp, hostname, metric, submetric, value) VALUES %s",
        value_list
    )
    conn.commit()
    cursor.close()
