import os
import sys
from fabric.api import *

HOST="127.0.0.1"
COMMAND="uname -a"

env.user = os.getenv('SSH_USER', 'kalyan')
env.password = os.getenv('SSH_PASSWORD', 'che')

@hosts(HOST)
def do_something():
    while True:
    	COMMAND = raw_input(HOST + ":>> ")    
    	run(COMMAND)
