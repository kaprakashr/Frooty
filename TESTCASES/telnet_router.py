#----------------- FROOTY AUTOMATION FRAMEWORK ---------------#
# TEST CASE FILE					      #
#-------------------------------------------------------------#
import sys
import os
import re

import_path = str(os.getcwd())
sys.path.append(import_path)
from src.libs.cisco.cisco_con import *
def TEST_CASE_001():
    log.rite("Starting Test Case 001\n")
    connect_to_cisco_device = telnet_connection(devices['DEVICE_1'])
    print connect_to_cisco_device.show_command('show version')
    log.rite(str(connect_to_cisco_device.show_command('show version')))
    return 1

def TEST_CASE_002():
    log.rite("Starting Test Case 002\n")
    connect_to_cisco_device = telnet_connection(devices['DEVICE_1'])
    log.rite(connect_to_cisco_device.configure_multiple_command(['int fastEthernet 2/0', 'ip address 1.1.1.1 255.0.0.0', 'end']))
    op = connect_to_cisco_device.show_command('show ip interface fastEthernet 2/0')
    log.rite(op)
    reg = re.compile('Internet address is\s(.*)')
    print "Internet address %s is configured properly" % reg.findall(op)[0]
    log.rite("Internet address " + reg.findall(op)[0] + " is configured properly")    
    return 1
