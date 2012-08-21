#!/usr/bin/python
import os, time
from subprocess import Popen, PIPE, STDOUT
fdir = '/root/tffile'
tdir = '/cl'

rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -mkdir %s'%(tdir), shell=True)
rcomm.communicate()


rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyFromLocal %s/eca482965e.log %s'%(fdir,tdir), shell=True)
rcomm.communicate()

rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -ls %s'%(tdir), shell=True)
rcomm.communicate()
