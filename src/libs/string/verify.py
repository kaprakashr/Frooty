#----------------- FROOTY AUTOMATION FRAMEWORK ---------------#
# Author        : Kalyana prakash Ravi/Saroj Mirdha
# Date          : 14/1/2017
# Version       : Base->Aadi

import re

def find(str1, str2):
    result = None
    reg = re.compile(str1)
    result = reg.search(str2)
    if result:
	return 1
    else:
	return 0
