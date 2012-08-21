#!/usr/bin/python
import os, time
import Queue
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
global q
q = Queue.Queue()
fdir = '/root/1tffile'
tdir = '/tffile'


def loadfile(fname,fdir,tdir):
	a = time.time()
	#rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyFromLocal '+fdir+'/'+fname+' '+tdir, shell=True)
	rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyFromLocal %s/%s %s'%(fdir,fname,tdir), shell=True)
	rcomm.communicate()
	b = time.time()
	elapsed = b - a
	q.put(elapsed)
	print '== File %s was copied in %f seconds' %(fname, elapsed )

lfname = os.listdir(fdir)

threads = []

k = 0
for n, v in enumerate(lfname):
	#bin/hadoop dfs -mkdir /tffile
	rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -mkdir %s%i'%(tdir,n), shell=True)
	rcomm.communicate()
	while k <= n:
		ttdir = tdir+str(n)
		t = Thread(target=loadfile, args=(lfname[k], fdir, ttdir,))
		t.start()
		threads.append(t)
		#print lfname[k]
		k += 1
	k = 0
	#print "n = %i"%(n)

print "before"
print threads
for thread in threads:
	thread.join()

print "after"
print threads

print "Threads are back"

aggregated_write_rate = 0
for elem in list(q.queue):
	aggregated_write_rate += 2 / elem

print "Aggregated write rate%f MB/s"%(aggregated_write_rate)
