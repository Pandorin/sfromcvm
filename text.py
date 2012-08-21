#!/usr/bin/python
import os, time
from threading import Thread
from subprocess import Popen, PIPE, STDOUT

def myfunc(i,s,st):
	#print "sleeping 5 sec from thread %d" % i
	#print s,st
	#time.sleep(5)
	#print "finished sleeping from thread %d" % i
	rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -ls /tffile', shell=True)
	rcomm.communicate()
	print '==== ==== ===='
	print i,st 
	print s

st = 'ddfdf'
lfname = os.listdir('/root/tffile')
for i in range(10):
	#print lfname[i]
	t = Thread(target=myfunc, args=(i,lfname[i],st,))
	t.start()
