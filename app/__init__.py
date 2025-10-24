from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
import requests
from DataAcq.Races import Races
from DataAcq.Drivers import drivers as drs

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
    

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/errors.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('PitCWRU startup')


@app.context_processor
def inject_season_races():
    try:
        races = Races.getCurrentYearRaceNames()
    except Exception:
        races = []

    return dict(races=races)

@app.context_processor
def inject_season_drivers():
    try:
        drivers = drs.get_current_season_driver_ids()
    except Exception:
        drivers = []
    
    return dict(drivers=drivers)

from app import routes, models, errors