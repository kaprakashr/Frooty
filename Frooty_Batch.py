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
import subprocess
#internal
from src.libs.cisco.cisco_con import *
from src.libs.logging.log import *
from src.libs.logging.print_log import *
import time
from datetime import datetime
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
    print ("[-B] [Filename] (or) [--case] [Filename]\n")
    print ("EXAMPLE: ") 
    print ("Froot_club.py -D \"DEVICES/Sample_Device.json\" -B \"BATCH_FILE/SMOKE_SANITY\"\n\n")
    exit(0)

#Exract Parmeters
catch_device = False
catch_case = False
for var in sys.argv:
    if re.match("-D",var) is not None or re.match("--device", var) is not None:
	catch_device = True
    elif re.match("-B",var) is not None or re.match("--case", var) is not None:
	catch_case = True
    elif catch_device == True:
	device_file = var
	catch_device = False
    elif catch_case == True:
	test_case_file = var
	catch_case = False 

reg_ignore_line = re.compile('#TESTCASES.*')
reg_testcase = re.compile('.*\/(.*)\.py')
reg_testcase_path = re.compile('(.*)\/.*\.py')
testcases = []
testcase_path = []
blocked_testcases = []
match_mod = None
file_dir = test_case_file
contents = open(file_dir, 'r')
tc_block = 0
for line in contents:
    if reg_ignore_line.findall(line):
	blocked_testcases += reg_testcase.findall(line)
	tc_block += 1
        continue
    testcases += reg_testcase.findall(line)
    testcase_path += reg_testcase_path.findall(line) 
contents.close()

total_pass_result = []
total_pass_log = []
total_fail_result = []
total_fail_log = []

for i in range(len(testcases)):
    #initialize the logging object
    ccwd = os.getcwd()
    log_folder = str(ccwd) + "/LOGS/"
    __builtin__.log = logger(log_folder, testcases[i])
    log = __builtin__.log
    Print("Init log->" + log_folder,log) 

    #Start
    if device_file == " " or test_case_file == " " or device_file == None or test_case_file == None:
        Print ("Please pass correct parameters \n",log)
        Print ("ERROR: \nEither Device or Test Case file is empty \n",log)
        exit(0)
    else:
	Print("SELECTED DEVICE FILE-> " + device_file + "\n" ,log)
	Print("SELECTED TEST CASE FILE-> " + test_case_file + "\n" ,log)
    
    with open(device_file) as data_file:
        device_data = json.load(data_file)
    
    #dump the device details
    Print("Loaded the Device file and starting now.,",log)
    Print("Jump to device file now.,",log)
    count = 1
    
    for device in device_data:
        if device_data[device].has_key("name") and device_data[device].has_key("ip") and device_data[device].has_key("port") and device_data[device].has_key("mode") and device_data[device].has_key("username") and device_data[device].has_key("password"):
            Print("DEVICE       :" + device,log)
            Print("NAME	     :" + device_data[device]["name"],log)
            Print("IP	        :" + device_data[device]["ip"],log)
            Print("PORT         :" + device_data[device]["port"],log)
            Print("MODE         :" + device_data[device]["mode"],log)
            Print("USER         :" + device_data[device]["username"],log)
            Print("PASS         :" + device_data[device]["password"],log)
            Print("COMM_STR     :" + device_data[device]["community_string"],log)
            Print("SNMP_PORT    :" + device_data[device]["snmp_port"],log)
        else:
    	    Print("Some Important parameter is missing , please check json file",log)
        count += 1
    #make the devices global
    __builtin__.devices = device_data
    
    #identify the test cases
    #TESTCASES/Sample_TestCase.py
    temp_load_module = testcase_path[0] + "." + testcases[i] 
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
	total_pass_result.append(total_pass)
        total_pass_log.append(log.fname)
        Print(str(method_to_call) + "-->RESULT: " + "PASSED",log,color=2)	
    elif result == False:
        total_fail += 1
	total_fail_result.append(total_fail)
 	total_fail_log.append(log.fname)
        Print(str(method_to_call) + "-->RESULT: " + "FAILED",log,color=3)
    else:
	pass
#Generate Consolidate Report 
reg_path_loc = re.compile('BATCH_FILE\/(.*)')
reg_path_loc.findall(test_case_file)[0]
cwd = os.getcwd()
summary_report_loc = str(cwd) + "/SUMMARY_REPORT/" + reg_path_loc.findall(test_case_file)[0] +"_"+ re.sub(r'\s+', '', datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) 

f = open(summary_report_loc, 'w')
f.write("<<<<<<<<<<<<<<SUMMARY OF RESULTS>>>>>>>>>>>>>>>\n")
f.write("TOTAL TEST CASES EXECUTED : " + str(len(total_pass_result)+len(total_fail_result)) + "\n")
f.write("TOTAL TEST CASES PASSED : " + str(len(total_pass_result)) + "\n")
f.write("=======LOG PATH========\n")
for i in range(len(total_pass_log)):
    f.write(str(i+1)+'.'+total_pass_log[i]+'\n')
f.write("TOTAL TEST CASES FAILED : " + str(len(total_fail_result)) + "\n")
f.write("=======LOG PATH========\n")
if total_fail_log != []:
    for j in range(len(total_fail_log)):
        f.write(str(j+1)+'.'+total_fail_log[j]+'\n')
else:
    f.write('NA\n')
f.write("TOTAL TEST CASES BLOCKED: " + str(tc_block) + "\n")
if blocked_testcases != []:
    for k in range(len(blocked_testcases)):
        f.write(str(k+1)+'.'+blocked_testcases[k]+'.py'+'\n')
else:
    f.write('NA\n')
f.close()

