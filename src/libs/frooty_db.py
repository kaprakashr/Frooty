#----------------- FROOTY AUTOMATION FRAMEWORK ---------------#
# Author        : Kalyana prakash Ravi
# Date          : 14/1/2017
# Version       : Base->Aadi

import sys
import re
import os
import time
from datetime import datetime
import sqlite3

#bug: it creates a new db, if the db_name is not existing, instead it should exit with error if db_name does not exist
def check_db_connection(db_location, db_name):
    temp = db_location + db_name
    connection = sqlite3.connect(temp)
    if connection:
	print "Connection Success\n"
        return 1
    else:
	print "Connection Failed\n"
	return 0

def insert_test_summary(db_location, db_name, input_data):
    input_data['DIGEST'] = True
    input_data['TEST_CASE_NAME'] = "None"
    input_data['id'] = 1
    input_data['STATUS'] = "SUCCESS"
    temp = db_location + db_name
    connection = sqlite3.connect(temp)
    if connection:
	connection.execute('INSERT INTO TEST_SUMMARY VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (input_data['id'], input_data['TEST_ID'], input_data['BATCH_NAME'], input_data['START_TIME'], input_data['TOPOLOGY_NAME'], input_data['FEATURES'], input_data['DIGEST'], input_data['STATUS'], input_data['PASS'], input_data['FAIL'], input_data['BLOCKED'], input_data['NEVER_RAN'], input_data['RUN_TIME'], input_data['TEST_CASE_NAME'], input_data['LOG_LOCATION']))
	connection.commit()
	connection.close()
	return 1
    else:
	return 0
