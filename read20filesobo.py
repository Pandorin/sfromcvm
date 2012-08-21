#!/usr/bin/python
import os, time
import Queue
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
global q

ptdir = '/tffile'

lfname = ['1ca8c50078.log', '0e9a382f32.log', '26c5fcc096.log', '11a69ebc70.log', 'fb54fe083b.log', '77c397ed11.log', '6be33c6936.log', '3c31c8e6e1.log', '1daa40c1eb.log', 'bdaf429100.log', '04b86f966d.log', '72552d5bde.log', 'af0b67ddfe.log', '669e21b97b.log', 'b200ab2009.log', 'eca596baaa.log', 'e2157ae0f5.log', '27bbdb2334.log', 'b96af3a2e1.log', '04ab7aed10.log']


def readfile(fname,fdir,tdir):
	a = time.time()
	rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyToLocal /20files%s/%s /root/tffile%s'%(fdir,fname,tdir), shell=True)
	rcomm.communicate()
	b = time.time()
	elapsed = b - a
	q.put(elapsed)
	print '== File %s was readed in %f seconds' %(fname, elapsed )

df = []
k = 0

for n, v in enumerate(lfname):
	q = Queue.Queue()
	threads = []
	fdir = ptdir+str(n)
	rcomm = Popen('mkdir /root/tffile%s'%(fdir), shell=True)
	rcomm.communicate()
	while k <= n:
		#ttdir = tdir+str(n)

		t = Thread(target=readfile, args=(lfname[k], fdir, fdir,))
		t.start()
		threads.append(t)
		k += 1

	print n
	for thread in threads:
		thread.join()

	aggregated_write_rate = 0
	for elem in list(q.queue):
		aggregated_write_rate += 40 / elem

	print "Aggregated write rate%f MB/s"%(aggregated_write_rate)
	df.append(aggregated_write_rate)
	k = 0

for l in df:
	print l
