#----------------- FROOTY AUTOMATION FRAMEWORK ---------------#
# Author        : Kalyana prakash Ravi/Saroj Mirdha
# Date          : 14/1/2017
# Version       : Base->Aadi

import sys
import json
import re
import os
from pprint import pprint
import importlib
#internal
from src.libs.cisco.cisco_con import *
from src.libs.logging.log import *
import __builtin__

#constant vars
device_file = None
test_case_file = None
__builtin__.log = None
device_data = None
__builtin__.devices = None

# FORMAT:
#	--help		: print the format
#	-D (or) --device: pass the devices file name
#	-T (or) --case  : pass test case file name
print ("\n----------------------------")
print ("| FROOTY AUTOMATION SUITE  |")
print ("----------------------------\n")
if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print ("\n----------------------------")
    print ("| FROOTY AUTOMATION SUITE  |")
    print ("----------------------------\n")
    print ("USAGE: ")
    print ("[-D] [Filename] (or) [--device] [Filename]")
    print ("[-T] [Filename] (or) [--case] [Filename]\n")
    print ("EXAMPLE: ") 
    print ("Froot_club.py -D \"DEVICES/Sample_Device.json\" -T \"TESTCASES/Sample_Test_Case.py\"\n\n")
    exit(0)

#Exract Parmeters
catch_device = False
catch_case = False
for var in sys.argv:
    if re.match("-D",var) is not None or re.match("--device", var) is not None:
	catch_device = True
    elif re.match("-T",var) is not None or re.match("--case", var) is not None:
	catch_case = True
    elif catch_device == True:
	device_file = var
	catch_device = False
    elif catch_case == True:
	test_case_file = var
	catch_case = False 

#initialize the logging object
ccwd = os.getcwd()
log_folder = str(ccwd) + "/LOGS/"
print ("Init log->" + log_folder)
__builtin__.log = logger(log_folder, test_case_file)
log = __builtin__.log

#Start
if device_file == " " or test_case_file == " " or device_file == None or test_case_file == None:
    print ("Please pass correct parameters \n")
    print ("ERROR: \nEither Device or Test Case file is empty \n")
    exit(0)
else:
    log.rite("SELECTED DEVICE FILE-> " + device_file + "\n")
    log.rite("SELECTED TEST CASE FILE-> " + test_case_file + "\n")

with open(device_file) as data_file:
    device_data = json.load(data_file)

#dump the device details
print("Loaded the Device file and starting now.,")
log.rite("Jump to device file now.,")
count = 1

for device in device_data:
    if device_data[device].has_key("name") and device_data[device].has_key("ip") and device_data[device].has_key("port") and device_data[device].has_key("mode") and device_data[device].has_key("username") and device_data[device].has_key("password"):
        log.rite("DEVICE      :", device)
        log.rite("NAME	      :" + device_data[device]["name"])
        log.rite("IP	      :" + device_data[device]["ip"])
        log.rite("PORT        :" + device_data[device]["port"])
        log.rite("MODE        :" + device_data[device]["mode"])
        log.rite("USER        :" + device_data[device]["username"])
        log.rite("PASS        :" + device_data[device]["password"])
        log.rite("COMM_STR    :" + device_data[device]["community_string"])
        log.rite("SNMP_PORT   :" + device_data[device]["snmp_port"])
    else:
	log.rite("Some Important parameter is missing , please check json file")
    count += 1
#make the devices global
__builtin__.devices = device_data

#identify the test cases
#TESTCASES/Sample_TestCase.py
match_mod = None
match_mod = re.match(r'(.*)\/(.*)\.py', test_case_file, re.M|re.I)
if match_mod == None:
    log.rite("Improper test case file.. Exiting.!\n")
    print ("ERROR: Test Case File\n" + "Please pass in this format-> TESTCASES/file_name.py")
    exit(0)
temp_load_module = match_mod.group(1) + "." + match_mod.group(2)
all_test_cases = importlib.import_module(temp_load_module)

#Now call all the test cases one by one automatically
#set all vars ahead of execution
total_ran = 0
total_pass = 0
total_fail = 0
total_block = 0
test_case_list = dir(all_test_cases)
result = None

for methods in test_case_list:
    if re.match("__",methods) is not None:
	junk = None
    elif re.match(".*[0-9]",methods) is not None and re.match("TEST",methods) is not None:
	total_ran += 1
    	method_to_call = getattr(all_test_cases,methods)
    	result = method_to_call()
 	if result == True:
	    total_pass += 1
	    log.rite(str(method_to_call) + "-->RESULT: " + "PASSED")	
	elif result == False:
	    total_fail += 1
	    log.rite(str(method_to_call) + "-->RESULT: " + "FAILED")
	else:
	    log.rite("ERROR: Please return 1 \(or\) 0 in your test case\n")
	    log.rite("ERROR: Results of this test case is not calculated for Regression/Smoke/Final results\n")
	    total_block += 1

#Now do the summary 
log.rite("\nTEST COMPLETED...!!\n")
log.rite("============================") 
log.rite("SUMMARY OF RESULTS")
log.rite("TOTAL TEST CASES RAN    : " + str(total_ran))
log.rite("TOTAL TEST CASES PASSED : " + str(total_pass))
log.rite("TOTAL TEST CASES FAILED : " + str(total_fail))
log.rite("TOTAL TEST CASES BLOCKED: " + str(total_block))
log.rite("============================\n")
log.rite("\n\n\n")
