#!/usr/bin/python
import md5, os, shutil, random
from subprocess import Popen, PIPE, STDOUT

nf = int(input("Enter number of files [int]: "))

rwdir = os.chdir('/root/tffile')
n = md5.new()
#n.update('sametextforgen')
#print n.hexdigest()

rcomm = Popen('pwd', shell=True)


#i=0
#while i < 20:
for i in xrange(0, nf):
	n.update('sametextforgenerate%d'%random.randrange (1,100))
	#i+=1
	scom = 'dd if=/dev/zero of=%s.log bs=1M count=40'%n.hexdigest()[0:10]
	rcomm = Popen(scom, shell=True)
	rcomm.communicate()
