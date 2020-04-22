import configparser
import sys
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')


def connect():
    return mysql.connector.connect(host=config['mysql']['host'],
                                   user=config['mysql']['user'],
                                   passwd=config['mysql']['passwd'],
                                   db=config['mysql']['db'])
