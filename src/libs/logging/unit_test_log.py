from log import logger

print "Start logging Unit Test"
log_obj = logger("/home/kalyan/FROOTY/LOGS/")
log_obj.rite("logging Unit Test Start\n")
var = "new variable"
#check multiple parameter pass
log_obj.rite("step 1: 2 params =" + var, "One more params")
log_obj.rite("step 2 = " + var, "One", "2", 3, "four")
for x in range(1,100):
	log_obj.rite("stress: " + "abcdefghijklmnopqrstuvwxyz")
log_obj.rite("logging Unit Test End\n")
