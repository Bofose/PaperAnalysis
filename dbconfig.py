import configparser
import pymysql
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')


def connect():
    return pymysql.connect(host=config['mysql']['host'],
                           user=config['mysql']['user'],
                           passwd=config['mysql']['passwd'],
                           db=config['mysql']['db'])
