import paramiko
import sys

nbytes = 4096
ip = 'localhost'
port = 22
username = 'kalyan' 
password = 'che'
cmd = 'pwd'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)
'''
stdin,stdout,stderr=ssh.exec_command(cmd)
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)
'''
while True:
    cmd = raw_input(ip + ":>>")
    stdin,stdout,stderr=ssh.exec_command(cmd)
    outlines=stdout.readlines()
    err=''.join(stderr.readlines())
    resp=''.join(outlines)
    print resp
    print err

ssh.close()
