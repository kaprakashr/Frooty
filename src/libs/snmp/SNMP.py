#!/usr/bin/python
from __future__ import print_function
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from pysnmp import debug

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
		print("\nSNMP COMMAND : " + "snmpget -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + oid[i] + "\n")
		snmp_data.append("\nSNMP COMMAND : " + "snmpget -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + oid[i] + "\n")
		print("<<<<<<<<<<<<OUTPUT>>>>>>>>>>>>>")
		snmp_data.append("<<<<<<<<<<<<OUTPUT>>>>>>>>>>>>>")
	        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		                                                        cmdgen.CommunityData(self.community_string),
		                                                        cmdgen.UdpTransportTarget(self.snmp_target),oid[i]
		                                                     )
                if errorIndication:
    	              snmp_data.append(varBinds)
		      break
                elif errorStatus:
    	              print('ERROR DETECTED: ');snmp_data.append('ERROR DETECTED: ')
    	              print('    %-16s %-60s' % ('error_message', errorIndication));snmp_data.append('    %-16s %-60s' % ('error_message', errorIndication))
    	              print('    %-16s %-60s' % ('error_status', errorStatus));snmp_data('    %-16s %-60s' % ('error_status', errorStatus))
    	              print('    %-16s %-60s' % ('error_index', errorIndex)); snmp_data.append('    %-16s %-60s' % ('error_index', errorIndex))
    	              return None
		else:
		    for varBind in varBinds:
			print(varBind);snmp_data.append(varBind)
	return snmp_data

    def snmpwalk(self,oid):
        '''This api is used for snmpwalk operation'''
	snmpwalk_result = []
	self.snmp_target = (self.host, self.snmp_port)
	if type(oid) == str and len(oid) == 1:
	    print("\nSNMP COMMAND : " + "snmpwalk -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + oid[0] + "\n")
	    snmpwalk_result.append("\nSNMP COMMAND : " + "snmpwalk -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + oid[0] + "\n")
	    print("<<<<<<<<OUTPUT>>>>>>>>>")
	    snmpwalk_result.append("<<<<<<<<OUTPUT>>>>>>>>>")
	    for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(),
                                                                 CommunityData(self.community_string),
                                                                 UdpTransportTarget(self.snmp_target),
                                                                 ContextData(),
                                                                 ObjectType(ObjectIdentity(oid)),
	                                       		     lexicographicMode=False):
                if errorIndication:
                    snmpwalk_result.append(errorIndication)
                    break
                elif errorStatus:
                    print('%s at %s' % (errorStatus.prettyPrint(),
                          errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                    break
                else:
                    for varBind in varBinds:
  			if varBind is None:
			    continue
			else:
                            print(varBind)
			    snmpwalk_result.append(varBind)
   	elif type(oid) == list and len(oid) >= 1:
	    for i in range(len(oid)):
		print("\nSNMP COMMAND : " + "snmpwalk -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + oid[i] + "\n")
		snmpwalk_result.append("\nSNMP COMMAND : " + "snmpwalk -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + oid[i] + "\n")
		print("<<<<<<<<OUTPUT>>>>>>>>>")
		snmpwalk_result.append("<<<<<<<<OUTPUT>>>>>>>>>")
	        for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(),
                                                                     CommunityData(self.community_string),
                                                                     UdpTransportTarget(self.snmp_target),
                                                                     ContextData(),
                                                                     ObjectType(ObjectIdentity(oid[i])),
                                                                 lexicographicMode=False):
                    if errorIndication:
                        snmpwalk_result.append(errorIndication)
                        break
                    elif errorStatus:
                        print('%s at %s' % (errorStatus.prettyPrint(),
                              errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                        break
                    else:
                        for varBind in varBinds:
			    if varBind is None:
			        continue
			    else:
                                print(varBind)
				snmpwalk_result.append(varBind)
	else:
	    pass
	return snmpwalk_result

    def snmpset(self,*args):
        '''This api is used for oid snmpset operation'''
	self.snmp_target = (self.host,self.snmp_port)
	cg = cmdgen.CommandGenerator()
	comm_data = cmdgen.CommunityData('my-manager', self.community_string)
	transport = cmdgen.UdpTransportTarget(self.snmp_target)
	snmpset_data = []
	for i in range(len(args[0])):
	    print("\nSNMP COMMAND : " + "snmpset -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + args[0][i][0] +' '+ args[0][i][2] +' '+args[0][i][1]+"\n")
	    snmpset_data.append("\nSNMP COMMAND : " + "snmpset -v2c -c " + self.community_string + ' ' + self.snmp_target[0] + ' ' + args[0][i][0] +' '+ args[0][i][2] +' '+args[0][i][1]+"\n")
	    print("<<<<<<<<OUTPUT>>>>>>>>>")
            snmpset_data.append("<<<<<<<<OUTPUT>>>>>>>>>")
	    if args[0][i][2] == "s":
	          variables = (args[0][i][0], rfc1902.OctetString(args[0][i][1]))
	          errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	          snmpset_data.append(result)
	    elif args[0][i][2] == "i":
	          variables = (args[0][i][0], rfc1902.Integer(args[0][i][1]))
	          errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	          snmpset_data.append(result)
	    elif args[0][i][2] == "o":
	          variables = (args[0][i][0], rfc1902.Bits(args[0][i][1]))
                  errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	          snmpset_data.append(result)
	    elif args[0][i][2] == "t":
	          variables = (args[0][i][0], rfc1902.TimeTicks(args[0][i][1]))
                  errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	          snmpset_data.append(result)
	    elif args[0][i][2] == "u":
	          variables = (args[0][i][0], rfc1902.Unsigned32(args[0][i][1]))
                  errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	          snmpset_data.append(result)
	    elif args[0][i][2] == "ip":
	          variables = (args[0][i][0], rfc1902.IpAddress(args[0][i][1]))
                  errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
   	          snmpset_data.append(result)
	    elif args[0][i][2] == "U":
	          variables = (args[0][i][0], rfc1902.Gauge32(args[0][i][1]))
                  errIndication, errStatus, errIndex, result = cg.setCmd(comm_data, transport,variables)
	          snmpset_data.append(result)
	    else:
	         pass

      	# Check for errors and print out results
	if errIndication:
	    print(errIndication)
	    snmpset_data.append(errIndication)
	elif errStatus:
	    print("REASON :" + '%s at %s' % (errStatus.prettyPrint(),errIndex and result[int(errIndex) - 1][0] or '?'))
	    snmpset_data.append("REASON : "+ '%s at %s' % (errStatus.prettyPrint(),errIndex and result[int(errIndex) - 1][0] or '?'))
	else:
	    for name, val in result:
	        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
		snmpset_data.append(name.prettyPrint() +" = "+ val.prettyPrint())	
        return snmpset_data
