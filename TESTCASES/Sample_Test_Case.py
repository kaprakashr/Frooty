#----------------- FROOTY AUTOMATION FRAMEWORK ---------------#
# TEST CASE FILE					      #
#-------------------------------------------------------------#
import sys
import os
import_path = str(os.getcwd())
sys.path.append(import_path)
from src.libs.cisco.cisco_con import *

# FOR BEGINNERS
# -------------
# How to call my device inside my test case function?
# ===================================================
#	It's simple! use the variable name "devices" to access the devices in the DEVICE folder
#	Example:
#	-------
#	>> ip_of_device_1 = devices['DEVICE_1']['ip']
#	>> connect_to_cisco_device = Cisco_Connection(devices['DEVICE_1'])	
#
# How to log the run and results?
# ==============================
#	As easy as below.!
#	>> log.rite("what ever I want to log")
#	>> log.rite("I need to pass few variables in log", variable_1, variable_2) 

def TEST_CASE_001():
    log.rite("Starting Test Case 001\n")
    print(devices['DEVICE_1'])

def TEST_CASE_002():
    log.rite("Starting Test Case 002\n")
    return 1
