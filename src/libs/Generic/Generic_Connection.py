#----------------- FROOTY AUTOMATION FRAMEWORK ---------------#
# Author        : Saroj Mirdha & Kalyana prakash Ravi
# Date          : 14/1/2017
# Version       : Base->Aadi

# BUG 1: Open: call disble paging in all the functions to aviod getting stuck

CMD_DELAY = 2

class generic_telnet_connection(object):
    '''This class is used to handle login,logout,cli command execution using telnet'''
    def __init__(self,dictionary):
	import telnetlib
	import time
	import re
	self.telnetlib = telnetlib
	self.time = time
	self.re = re
	self.copy = dictionary
	self.ip = str(dictionary['ip'])
	self.port = int(dictionary['port'])
        self.username = str(dictionary['username'])
        self.password = str(dictionary['password'])
	self.delay = CMD_DELAY

    def connect(self):
	'''This function is used for create telnet sesssion to Router'''
	try:
	   self.telnet = self.telnetlib.Telnet(self.ip, self.port)
	   login_prompt = self.telnet.read_until("\(Username: \)|\(login: \)", self.delay)
	   if 'login' in login_prompt:
	       self.telnet.write(self.username+'\n')
	   elif 'Username' in login_prompt:
	       self.telnet.write(self.username+'\n')
	   password_prompt = self.telnet.read_until("Password: ", self.delay)
	   if 'Password' in password_prompt:
	       self.telnet.write(self.password+'\n')
	   return self.telnet
	except Exception as err:
	    print "Error : %s" % err

    def close(self):
	'''This API is used for closing telnert session'''
	return self.telnet.close()
    
    def disable_paging(self,command='terminal length 0'):
	'''This API is used to set your terminal to display without any breaks in privileged mode'''
	self.telnet.write(command+'\r\r\n')
	return self.telnet.read_until("\(#\)|\(>\)", self.delay)

    def show_command(self,command):
        '''This API is used execute RAW commands'''
	try:
	    self.connect()
	    if self.telnet != None:
	       self.time.sleep(self.delay)
	       self.telnet.write("\r\n\r\n")
	       if type(command) == str:
	           self.telnet.write(command+'\r\n')
	       elif type(command) == list:
	           for cmd in command:
	               self.telnet.write(cmd+'\r\n')
	               self.time.sleep(self.delay)
		   self.close()
	       return self.telnet.read_until(".*[#|>]\r\n",self.delay)
	    else:
	        print "Error : Telent session is not established"
	except Exception as err:
	    print "Error : %s" % err

    def configure_multiple_command(self,commands_list):
	'''This API is used to configure multiple set of cli commands'''
	try:
	    self.connect()
	    if self.telnet != None:
	       self.time.sleep(self.delay)
	       self.telnet.write("\r\n\r\n")
	       for cmd in commands_list:
	           self.telnet.write(cmd+"\r\n")
	       self.close()
	       return self.telnet.read_until(".*#\r\n",self.delay)
	    else:
	        print "Error : Telnet session is not established"
	except Exception as err:
	    print "Error : %s" % err

class generic_ssh_connection(object):
    '''This class is used to handle login,logout,cli command execution using ssh'''
    def __init__(self,dictionary):
        import paramiko
        import time
        import re
        self.paramiko = paramiko
        self.time = time
        self.re = re
	self.copy = dictionary
        self.ip = str(dictionary['ip'])
        self.port = int(dictionary['port'])
	self.buffer = 65535
        self.username = str(dictionary['username'])
        self.password = str(dictionary['password'])
        self.delay = CMD_DELAY

    def connect(self):
       '''This function is used for create ssh sesssion to Router'''
       try:
	   self.ssh = self.paramiko.SSHClient() 
	   self.ssh.set_missing_host_key_policy(self.paramiko.AutoAddPolicy())
	   self.ssh.connect(self.ip, username=self.username, password=self.password, allow_agent=False,look_for_keys=False, port=self.port)
	   self.ssh_conn = self.ssh.invoke_shell()		
	   self.time.sleep(float(self.delay))
	   return self.ssh_conn.recv(self.buffer)
       except Exception as err:
           print "Error : %s" % err

    def close(self):
	'''This API is used for closing ssh sessions'''
	self.ssh_conn.close()

    def clear_buffer(self):
        if self.ssh_conn.recv_ready():
            return self.ssh_conn.recv(self.buffer)
        else:
	    return None

    def disable_paging(self, command='terminal length 0'):
	'''This API is used to set your terminal to display without any breaks in privileged mode'''
	self.ssh_conn.send(command+'\r\r\n')

    def show_command(self,command):
        '''This API is used execute show commands'''
	try:
            session_op = self.connect()
            if self.ssh_conn != None:
               self.time.sleep(self.delay)
               self.ssh_conn.send("\r\n\r\n")
               if type(command) == str:
                   self.ssh_conn.send(command+'\r\n')
		   self.time.sleep(self.delay)
               elif type(command) == list:
                   for cmd in command:
                       self.ssh_conn.send(cmd+'\r\n')
                       self.time.sleep(self.delay)
	       if self.ssh_conn.recv_ready():
		    self.close()
                    return self.ssh_conn.recv(self.buffer)
            else:
                print "Error : ssh session is not established"
	except Exception as err:
	    print "Error : %s" % err

    def configure_command(self,command):
        '''This API is used to configure command in privileged mode'''
	try:
	    session_op = self.connect()
	    if session_op != None:
	       self.time.sleep(self.delay)
	       self.ssh_conn.send("\r\n\r\n") 
	       self.ssh_conn(command+'\r\n')
	       self.time.sleep(self.delay)
	       if self.ssh_conn.recv_ready():
		   self.close()
	           return self.ssh_conn.recv(self.buffer)
	    else:
	        print "Error : ssh session is not established"
	except Exception as err:
	    print "Error : %s" % err
	
    def configure_multiple_command(self,commands_list):
       '''This API is used to configure multiple set of cli commands'''
       try:
           session_op = self.connect()
           if session_op != None:
               self.time.sleep(self.delay)
               self.ssh_conn.send("\r\n\r\n")
               if type(commands_list) == str:
                   self.ssh_conn.send(command_list+'\r\n')
		   self.time.sleep(self.delay)
               if type(commands_list) == list:
                   for command in range(len(commands_list)):
                       self.ssh_conn.send(commands_list[command]+'\r\n')
            	       self.time.sleep(self.delay)
               if self.ssh_conn.recv_ready():
		   self.close()
                   return self.ssh_conn.recv(self.buffer)
           else:
               print "Error : ssh is not established"	
       except Exception as err:
           print "Error : %s" % err
