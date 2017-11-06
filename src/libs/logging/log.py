#----------------- FROOTY AUTOMATION FRAMEWORK ---------------#
# Author	: Kalyana prakash Ravi
# Date		: 14/1/2017
# Version	: Base->Aadi

import sys
import re
import os
import time
from datetime import datetime
from src.libs.logging.print_log import start_time,end_time,total_time_taken

#Basic logging class
class logger:
    fname = ""
    log_loc = ""
    fhandle = ""

    #give the log file location when you take an instance of the logging class
    def __init__(self,log_location,name):
	self.log_loc = log_location
	name_tmp = name.split(".")
	name_tmp = name_tmp[0].split("/")
	self.fname = self.log_loc + name_tmp[-1] + "_" + re.sub(r'\s+', '', datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))  + ".log"	
	self.fhandle = open(self.fname,'w')
	#self.fhandle.write("FROOTY->STARTING RUN: 	" + re.sub(r'\s+', '', datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + "\n\n")
       
    def rite(self,*args):
	temp_str = ""
	temp_str_list = []
        stamp = "[" + time.strftime("%H:%M:%S") + "]: "
	for varg in args:
	    if str(varg) == "":
		varg = None #nothing
	    else:
	        temp_str_list.append(str(varg))
		#print ("arg:  " + str(varg) + "\n")
	temp_str = ' '.join(temp_str_list)
        self.fhandle.write(stamp + temp_str + "\n")
        return 1

    def start_test_case(self,desc=None,steps=None,pass_criteria=None):
        temp = "----"*10 + "\n"
        temp = temp + "--" + "DESRIPTION: " + desc + "\n"
        temp = temp + "--" + "STEPS: " + steps + "\n"
        temp = temp + "--" + "PASS CRITERION: " + pass_criteria + "\n"
        temp = temp + "----"*10 + "\n\n"
        self.fhandle.write(temp)
        return 1

    def __del__(self):
        self.fhandle.close()
