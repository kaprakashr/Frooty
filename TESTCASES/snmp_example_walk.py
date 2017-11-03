import sys
import os
import re
import_path = str(os.getcwd())
sys.path.append(import_path)
from src.libs.cisco.cisco_con import *
from src.libs.string.verify import *
from src.libs.snmp.SNMP import *
from print_log import *

def TEST_CASE_001():
    obj = snmpwalker(devices['DEVICE_1'])
    op = obj.snmpwalk(['.1.3.6.1.2.1.1'])
    for i in op:
         Print(i,log)
    return 1


'''
NOTE:-
SNMP MIB OID name not supporting, So Use MIB OID number for snmpwalk/snmpget/snmpset operation
and also SNMPv1 and SNMPv2c currently supported
'''
