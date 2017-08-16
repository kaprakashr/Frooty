import sys
import os

importpath = str(os.getcwd())
sys.path.append(import_path)
from src.libs.cisco.cisco_con import *


def TEST_CASE_001():
    log.rite("Starting Testcase 001\n")
    connect_to_cisco_device = ssh_connection(devices['DEVICE_1'])
    print connect_to_cisco_device.show_command('show version')
    
    
