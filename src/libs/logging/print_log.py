import datetime
import time
import re
from colored import *

def Print(msg, logging=None , color=None):
    if color != None:
	print(fg(0) + bg(color) + msg + attr(0) + "\n")
    if logging != None:
        logging.rite(msg)


def start_time():
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reg_time = re.compile('.*\s+(\d+\:\d+\:\d+)')
    st_time = reg_time.findall(start_time)[0]
    return (start_time , st_time)


def end_time():
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reg_time = re.compile('.*\s+(\d+\:\d+\:\d+)')
    en_time = reg_time.findall(end_time)[0]
    return (end_time , en_time)

def total_time_taken(en_time,st_time):
    total_time=(datetime.datetime.strptime(en_time,'%H:%M:%S') - datetime.datetime.strptime(st_time,'%H:%M:%S'))
    return total_time

