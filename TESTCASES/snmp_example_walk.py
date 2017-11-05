import sys
import os
import re
import_path = str(os.getcwd())
sys.path.append(import_path)
from src.libs.cisco.cisco_con import *
from src.libs.string.verify import *
from src.libs.snmp.SNMP import *
from src.libs.logging.print_log import *

def TEST_CASE_001():
    try:
        obj = snmpwalker(devices['DEVICE_1'])
        op = obj.snmpwalk(['.1.3.6.1.2.1.1'])
        for i in op:
             Print(i,log)
    except Exception as err:
	Print(err,log)
    return 1


def TEST_CASE_002():
    try:
        obj = snmpwalker(devices['DEVICE_1'])
        op = obj.snmpwalk(['.1.3.6.1.2.1.1'])
        for i in op:
             Print(i,log)
    except Exception as err:
	Print(err,log)
    return 1

'''
NOTE:-
SNMP MIB OID name not supporting, So Use MIB OID number for snmpwalk/snmpget/snmpset operation
and also SNMPv1 and SNMPv2c currently supported
'''
