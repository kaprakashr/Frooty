import sys
import os
import re

import_path = str(os.getcwd())
sys.path.append(import_path)
from src.libs.cisco.cisco_con import *
from src.libs.snmp.SNMP import *
from src.libs.string.verify import *

def TEST_CASE_001():
    log.rite("Starting Test Case 001\n")
    obj = snmpwalker(DEVICE_1)
    print("######snmpget operation#####")
    ob = obj.snmpget(['1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.6.0'])
    print(ob)
    print("######snmpwalk operation######") 
    op = obj.snmpwalk('.1.3.6.1.2.1.1')
    print(op)
    print("#####snmpset operation######")
    result = obj.snmpset('1.3.6.1.2.1.1.1.0' , 'new_Comment' , "s")


'''
NOTE:-
SNMP MIB OID name not supporting, So Use MIB OID number for snmpwalk/snmpget/snmpset operation
and also SNMPv1 and SNMPv2c currently supported
'''
