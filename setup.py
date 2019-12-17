from setuptools import setup

setup(name='aiven-kafka-psql',
      version='0.1',
      description='Collects system metrics, sends them though Kafka and ultimately stores them in PostgreSQL',
      url='http://github.com/tuomasjaanu/aiven-kafka-psql',
      author='Tuomas Jaanu',
      author_email='tuomas.jaanu@gmail.com',
      license='MIT',
      packages=['aiven_kafka_psql','aiven_kafka_psql.impl'],
      zip_safe=False,
      entry_points={
          'console_scripts': ['aiven-collect=aiven_kafka_psql.collect_metrics:main',
                              'aiven-psql=aiven_kafka_psql.upload_to_psql:main'],
      }
      )
