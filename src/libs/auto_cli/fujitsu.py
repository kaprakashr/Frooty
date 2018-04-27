import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
import paramiko
import sys

nbytes = 4096
ip = '167.254.219.241'
port = 26004
username = 'fujitsu'
password = '1finity'
cmd = "\n\n"

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password,look_for_keys=False,allow_agent=False)
'''
stdin,stdout,stderr=ssh.exec_command(cmd)
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)
'''
cflag = False
while True:
    if 'configure' in cmd:
        cflag = True
    elif cflag is True and 'exit' in cmd:
        cflag = False
    if cflag is True:
        if cmd.strip() == 'configure':
            cmd = 'configure'
        else:
            cmd = "configure \r\n" + cmd
        stdin,stdout,stderr=ssh.exec_command(cmd)
        outlines=stdout.readlines()
        err=''.join(stderr.readlines())
        resp=''.join(outlines)
        print resp
        print err
        cmd = raw_input(username + '@' + ip + ":[Configure]%")
    else:
        stdin,stdout,stderr=ssh.exec_command(cmd)
        outlines=stdout.readlines()
        err=''.join(stderr.readlines())
        resp=''.join(outlines)
        print resp
        print err
        cmd = raw_input(username + '@' + ip + ":[Access]>")

ssh.close()
