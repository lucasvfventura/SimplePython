from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from python_kafka_logging.KafkaHandler import KafkaLoggingHandler
# from logging import getLogger, FileHandler, Formatter
#
from config import config
import os

environment = os.getenv('SIMPLEWEB_CONFIG', 'default')

db = SQLAlchemy()

app = Flask(__name__)

# app.config.from_object(config[environment])
app.config.from_object(config['development'])

# Configure logging
# kafkaLog = getLogger('simpleweb')
# kafka_handler = KafkaLoggingHandler(app.config['LOGGING_TO_KAFKA_HOST'], app.config['LOGGING_TO_KAFKA_TOPIC'])
# kafka_handler.setLevel(app.config['LOGGING_LEVEL'])
# kafka_handler.setFormatter(formatter)
# kafkaLog.addHandler(kafka_handler)

# fileLog = getLogger('simpleweb')
# file_handler = FileHandler(app.config['LOGGING_TO_FILE'])
# file_handler.setLevel(app.config['LOGGING_LEVEL'])
# formatter = Formatter(app.config['LOGGING_FORMAT'])
# file_handler.setFormatter(formatter)
# fileLog.addHandler(file_handler)

db.init_app(app)

import simpleweb.api
import simpleweb.models