import sys
import os
import re

import_path = str(os.getcwd())
sys.path.append(import_path)
from src.libs.cisco.cisco_con import *
from src.libs.Generic.Generic_Connection import *

def TEST_CASE_001():
    log.rite("Starting Test Case 001\n")
    connect_to_generic_device = generic_telnet_connection(devices['DEVICE_1'])
    print connect_to_generic_device.show_command('show version')
    log.rite(str(connect_to_generic_device.show_command('show version')))
    return 1

def TEST_CASE_002():
    log.rite("Starting Test Case 002\n")
    connect_to_generic_device = generic_telnet_connection(devices['DEVICE_1'])
    log.rite(connect_to_generic_device.configure_multiple_command(['ls -l', 'ls -lrt']))
    op = connect_to_generic_device.show_command('ls')
    log.rite(op)
    reg = re.compile('(.*)')
    log.rite(">> is configured properly")
    return 1

def TEST_CASE_003():
    log.rite("Starting Test Case 003\n")
    connect_to_generic_device = generic_ssh_connection(devices['DEVICE_1'])
    print connect_to_generic_device.show_command('show version')
    log.rite(str(connect_to_generic_device.show_command('show version')))
    return 1

def TEST_CASE_004():
    log.rite("Starting Test Case 004\n")
    connect_to_generic_device = generic_ssh_connection(devices['DEVICE_1'])
    log.rite(connect_to_generic_device.configure_multiple_command(['ls -l', 'ls -lrt']))
    op = connect_to_generic_device.show_command('ls')
    log.rite(op)
    reg = re.compile('(.*)')
    log.rite(">> is configured properly")
    return 1

