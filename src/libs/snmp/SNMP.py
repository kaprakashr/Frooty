#!/usr/bin/python
from __future__ import print_function
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

#NOTE#
##Currently SNMPv1 and SNMPv2c supported###

class snmpwalker(object):
    '''This class is used for snmpwalk , snmpget, snmpset operation'''
    def __init__(self,dictionary):
        self.copy = dictionary
        self.host = str(dictionary['ip'])
	self.community_string = str(dictionary['community_string'])
	self.snmp_port = int(dictionary['snmp_port'])

    def extract_data(self,data):
        sn_data = []
	for i in range(len(data)):
            for name, val in data[i]:
                sn_data.append(name.prettyPrint() +" = "+ val.prettyPrint())
	return sn_data

    def snmpget(self,oid):
        '''This api is used for snmpget operation''' 
	global extract_data
        self.snmp_target = (self.host, self.snmp_port)
        display_errors = None
	snmp_data = []
        # Create a PYSNMP cmdgen object
       	cmdGen = cmdgen.CommandGenerator()
	if type(oid) == list and len(oid) >= 1:
	    for i in range(len(oid)):
	        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		                                                        cmdgen.CommunityData(self.community_string),
		                                                        cmdgen.UdpTransportTarget(self.snmp_target),oid[i]
		                                                        )
                if not errorIndication:
    	              snmp_data.append(varBinds)
                else:
		      display_errors = True
    	              if display_errors:
    	                  print('ERROR DETECTED: ')
    	                  print('    %-16s %-60s' % ('error_message', errorIndication))
    	                  print('    %-16s %-60s' % ('error_status', errorStatus))
    	                  print('    %-16s %-60s' % ('error_index', errorIndex))
    	              return None
	return self.extract_data(snmp_data)

    def snmpwalk(self,oid):
        '''This api is used for snmpwalk operation'''
	self.snmp_target = (self.host, self.snmp_port)
	for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(),
                                                             CommunityData(self.community_string),
                                                             UdpTransportTarget(self.snmp_target),
                                                             ContextData(),
                                                             ObjectType(ObjectIdentity(oid)),
	                                   		     lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                      errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    print(varBind)
    
    def snmpset(self,oid,new_val,snmp_type):
        '''This api is used for oid snmpset operation'''
	self.snmp_target = (self.host,self.snmp_port)
	cg = cmdgen.CommandGenerator()
	comm_data = cmdgen.CommunityData('my-manager', self.community_string)
	transport = cmdgen.UdpTransportTarget(self.snmp_target)
	if snmp_type == "s":
	      variables = (oid, rfc1902.OctetString(new_val))
	      errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	elif snmp_type == "i":
	      variables = (oid, rfc1902.Integer(new_val))
	      errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	elif snmp_type == "o":
	      variables = (oid, rfc1902.Bits(new_val))
              errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	elif snmp_type == "t":
	      variables = (oid, rfc1902.TimeTicks(new_val))
              errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	elif snmp_type == "u":
	      variables = (oid, rfc1902.Unsigned32(new_val))
              errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	elif snmp_type == "ip":
	      variables = (oid, rfc1902.IpAddress(new_val))
              errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	elif snmp_type == "U":
	      variables = (oid, rfc1902.Gauge32(new_val))
              errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	else:
	     pass


      	# Check for errors and print out results
	snmp_set_data = []
	if errIndication:
	    print(errIndication)
	elif errStatus:
	    print('%s at %s' % (errStatus.prettyPrint(),errIndex and result[int(errIndex) - 1][0] or '?'))
	else:
	    for name, val in result:
	        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
		     snmp_set_data.append(name.prettyPrint() +" = "+ val.prettyPrint())	
	    return snmp_set_data
