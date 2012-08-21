#!/usr/bin/python
import os, time
import Queue
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
global q

fdir = '/root/tffile'
ptdir = '/tffile'


a = time.time()
rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyToLocal /20files/tffile19 /root/tffile', shell=True)
rcomm.communicate()
b = time.time()
elapsed = b - a

print elapsed
print 2000/elapsed
