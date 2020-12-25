# data acqusition module 

import csv
#import pandas as pd 
from init import *
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def init_db(database):
    # database = r"data\pythonsqlite2.db"    
    tables = [
    """ CREATE TABLE IF NOT EXISTS `data` (
	`sys_id`	INTEGER NOT NULL,
	`timestamp`	TEXT NOT NULL,
	`value`	TEXT NOT NULL,
	FOREIGN KEY(`value`) REFERENCES `iot_devices`(`sys_id`)
    );""",
    """CREATE TABLE IF NOT EXISTS `iot_devices` (
	`sys_id`	INTEGER NOT NULL UNIQUE,
	`name`	TEXT,
	`type_id`	INTEGER NOT NULL UNIQUE,
	`place_id`	INTEGER NOT NULL UNIQUE,
	`status`	TEXT,
    `units`	TEXT,
	`last_updated`	TEXT,
	`update_interval`	INTEGER,
	PRIMARY KEY(`sys_id`),
    FOREIGN KEY(`place_id`) REFERENCES `place`(`place_id`),	
	FOREIGN KEY(`type_id`) REFERENCES `type`(`type_id`)
    ); """,    
    """CREATE TABLE IF NOT EXISTS `place` (
	`place_id`	INTEGER NOT NULL,
	`block`	TEXT,
	`building`	TEXT,
	`room`	TEXT,
	`placed`	TEXT,
	PRIMARY KEY(`place_id`)
    ); """,
    """CREATE TABLE IF NOT EXISTS `type` (
	`type_id`	INTEGER NOT NULL UNIQUE,
	`name`	TEXT,
	`enabled`	INTEGER,    
	`state`	TEXT,
	`mode`	TEXT,
	`fan`	TEXT,
	`temperature`	REAL,
	`special`	TEXT,
	PRIMARY KEY(`type_id`)	
    ); """    
    ]
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        for table in tables:
            create_table(conn, table)        
    else:
        print("Error! cannot create the database connection.")


def csv_acq_data():
        conn= create_connection(db_name)
        
        try:
            if db_init:                
                data = pd.read_csv("data/homedata.csv")
                data.to_sql(table_name, conn, if_exists='append', index=False)                       
            else:
                data = pd.read_sql_query("SELECT * FROM "+table_name, conn)
        except Error as e:
            print(e)
        finally:    
            if conn:
                conn.close()    

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid





if __name__ == '__main__':
    if db_init:
        init_db(db_name)     


# if __name__ == "__main__":    
#     data = acq_data()
#     # Preview the first 5 lines of the loaded data 
#     print(data.head())
