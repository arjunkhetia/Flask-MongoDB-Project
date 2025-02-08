from flask_pymongo import PyMongo
from flask import Flask
import configparser

config = configparser.ConfigParser()
config.read("config/app-config.cfg")

mongo = PyMongo()

def init_db(app: Flask):
    app.config["MONGO_URI"] = config["DATABASE"]["MONGO_URI"]
    mongo.init_app(app)