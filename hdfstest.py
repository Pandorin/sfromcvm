#!/usr/bin/python
import os, time
import Queue
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
tdir = '/tf'

for n in range(0,8):
	rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -mkdir %s%i'%(tdir,n), shell=True)
	rcomm.communicate()
