#!/usr/bin/python
import os, time
import Queue
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
global q
q = Queue.Queue() 
fdir = '/root/tffile'
tdir = '/tffile'

def loadfile(fname,fdir,tdir):
	a = time.time()
        rcomm = Popen('/usr/local/hadoop/bin/hadoop dfs -copyFromLocal '+fdir+'/'+fname+' '+tdir, shell=True)
        rcomm.communicate()
	b = time.time()
        elapsed = b - a 
        q.put(elapsed)
        print '== File %s was copied in %f seconds' %(fname, elapsed )


lfname = os.listdir(fdir)
ttdir = tdir+str(len(lfname))
threads = []
for fname in lfname:
        t = Thread(target=loadfile, args=(fname, fdir, ttdir,))
        t.start()
        threads.append(t)

print "before"
print threads
for thread in threads:
    thread.join()

print "after"
print threads

print "Threads are back"
df = []

aggregated_write_rate = 0
for elem in list(q.queue):
	df.append(elem)
	aggregated_write_rate += 2 / elem

print "Aggregated write rate%f MB/s"%(aggregated_write_rate)
df.append("Aggregated write rate: %f"%(aggregated_write_rate))

f = open('result%i.log'%(len(lfname)), 'w')
ldf = len(df)
for i in range(0,ldf):
	f.write("%s\n"%(str(df[i])))
f.close()
#print ' ========= Results writed in file: result%i.log'%(len(lfname))
print df
