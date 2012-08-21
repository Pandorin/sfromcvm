#!/usr/bin/python
import os, time
import Queue
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
global q

fdir = '/root/tffile'
ptdir = '/tffile'

lfname = os.listdir(fdir)

tdir = '/%ifiles%s'%(len(lfname),ptdir)

def loadfile(fname,fdir,tdir):
	a = time.time()
	#rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyFromLocal '+fdir+'/'+fname+' '+tdir, shell=True)
	rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyFromLocal %s/%s %s'%(fdir,fname,tdir), shell=True)
	rcomm.communicate()
	b = time.time()
	elapsed = b - a
	q.put(elapsed)
	print '== File %s was copied in %f seconds' %(fname, elapsed )

df = []
k = 0
for n, v in enumerate(lfname):
	q = Queue.Queue()
	threads = []
	rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -mkdir %s%i'%(tdir,n), shell=True)
	rcomm.communicate()
	while k <= n:
		ttdir = tdir+str(n)
		t = Thread(target=loadfile, args=(lfname[k], fdir, ttdir,))
		t.start()
		threads.append(t)
		k += 1
		
	#print "before"
	#print threads
	print n
	for thread in threads:
		thread.join()

	#print "after"
	#print threads
	
	#print "Threads are back"

	aggregated_write_rate = 0
	for elem in list(q.queue):
		aggregated_write_rate += 20 / elem

	print "Aggregated write rate%f MB/s"%(aggregated_write_rate)
	df.append(aggregated_write_rate)
	k = 0
for l in df:
	print l

