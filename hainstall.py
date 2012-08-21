#!/usr/bin/python
import os, shutil
from subprocess import Popen, PIPE, STDOUT

wdir = '/usr/local/'
gdfile = 'wget http://mirror.switch.ch/mirror/apache/dist/hadoop/common/hadoop-1.0.3/hadoop-1.0.3-bin.tar.gz'
dfile = 'hadoop-1.0.3-bin.tar.gz'
vhdfs = '/app/hadoop/tmp'
print '== Variables are set\n'

rwdir = os.chdir(wdir)
print '== Directory is changed'

rcomm = Popen([gdfile], shell=True)
rcomm.communicate()
print '== File is downloaded'

rcomm = Popen('tar vxf hadoop-1.0.3-bin.tar.gz', shell=True)
rcomm.communicate()
print '== Files is unpacked'

rcomm = os.rename('hadoop-1.0.3', 'hadoop')
print '== Directory is renamed'

print '=======================\n'

rcomm = Popen('mkdir -p '+vhdfs, shell=True)
print '== Directory for HDFS is created'

print '======================\n'

print 'Work with /conf/* files'

dipdir = wdir+'hadoop/conf/'
print '== Var are set'
rwdir = os.chdir(dipdir)
print '== Dir is changed'
i = 0
f = open('hadoop-env.sh','r')
flines = f.readlines()
h = len(flines)
n=range(h+1)
for fline in flines:
        if '# Extra Java runtime options.  Empty by default.' in fline:
                n[i] = fline
                i += 1
                n[i] = 'export HADOOP_OPTS=-Djava.net.preferIPv4Stack=true\n'
        else:
                n[i] = fline
        i += 1
print n

f.close()

f = open('hadoop-env.sh','w')
f.write(''.join(n))
f.close()
print '== hadoop-env.sh is changed'

coresite = ['<?xml version="1.0"?>\n', '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n', '\n', '<!-- Put site-specific property overrides in this file. -->\n', '\n', '<configuration>\n', '<property>\n', '  <name>hadoop.tmp.dir</name>\n', '  <value>'+vhdfs+'</value>\n', '  <description>A base for other temporary directories.</description>\n', '</property>\n', '\n', '<property>\n', '  <name>fs.default.name</name>\n', '  <value>hdfs://master:54310</value>\n', '  <description>The name of the default file system.  A URI whose\n', '  scheme and authority determine the FileSystem implementation.  The\n', "  uri's scheme determines the config property (fs.SCHEME.impl) naming\n", "  the FileSystem implementation class.  The uri's authority is used to\n", '  determine the host, port, etc. for a filesystem.</description>\n', '</property>\n', '</configuration>']

f = open('core-site.xml','w')
f.write(''.join(coresite))
f.close()
print '== core-site.xml is changed'

mapredsite = ['<?xml version="1.0"?>\n', '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n', '\n', '<!-- Put site-specific property overrides in this file. -->\n', '\n', '<configuration>\n', '<property>\n', '  <name>mapred.job.tracker</name>\n', '  <value>localhost:54311</value>\n', '  <description>The host and port that the MapReduce job tracker runs\n', '  at.  If "local", then jobs are run in-process as a single map\n', '  and reduce task.\n', '  </description>\n', '</property>\n', '</configuration>\n']
f = open('mapred-site.xml','w')
f.write(''.join(mapredsite))
f.close()
print '== mapred-site.xml is changed'

hdfssite = ['<?xml version="1.0"?>\n', '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n', '\n', '<!-- Put site-specific property overrides in this file. -->\n', '\n', '<configuration>\n', '<!-- In: conf/hdfs-site.xml -->\n', '<property>\n', '  <name>dfs.replication</name>\n', '  <value>1</value>\n', '  <description>Default block replication.\n', '  The actual number of replications can be specified when the file is created.\n', '  The default is used if replication is not specified in create time.\n', '  </description>\n', '</property>\n', '</configuration>\n']
f = open('hdfs-site.xml','w')
f.write(''.join(hdfssite))
f.close()
print '== hdfs-site.xml is changed'


# Work with .bashrc file 
def bashrc (hadoop_dir):
        javah = '/usr/lib/jvm/java-1.6.0-openjdk-1.6.0.0.x86_64'
        #make a backup copy of .bashrc
        shutil.copy('/root/.bashrc','/root/.bashrc_old')
        #check if there is a standard path to Java(1.6.0)
        if os.path.exists(javah):
                print ' == Java(1.6.0) dir -yes'
                add_in_bashrc(1,hadoop_dir,javah)
        else:
                print ' == Java(1.6.0) dir -no'
                add_in_bashrc(0,hadoop_dir,javah)

def add_in_bashrc(java_dir,hadoop_dir,javah):
        f = open('/root/.bashrc','r')
        flines = f.readlines()
        f.close()
        if java_dir == 1:
                addinf = ['# Set Hadoop-related environment variables\n', 'export HADOOP_HOME='+hadoop_dir+'\n', '\n', '# Set JAVA_HOME (we will also configure JAVA_HOME directly for Hadoop later on)\n', 'export JAVA_HOME='+javah+'\n', '\n', '# Some convenient aliases and functions for running Hadoop-related commands\n', 'unalias fs &> /dev/null\n', 'alias fs="hadoop fs"\n', 'unalias hls &> /dev/null\n', 'alias hls="fs -ls"\n', '\n', '# Add Hadoop bin/ directory to PATH\n', 'export PATH=$PATH:$HADOOP_HOME/bin:'+javah+'/bin\n', '\n']
        elif java_dir == 0:
                addinf = ['# Set Hadoop-related environment variables\n', 'export HADOOP_HOME='+hadoop_dir+'\n', '\n', '# Set JAVA_HOME (we will also configure JAVA_HOME directly for Hadoop later on)\n', '# export JAVA_HOME=<JAVA_HOEN_DIR>\n', '\n', '# Some convenient aliases and functions for running Hadoop-related commands\n', 'unalias fs &> /dev/null\n', 'alias fs="hadoop fs"\n', 'unalias hls &> /dev/null\n', 'alias hls="fs -ls"\n', '\n', '# Add Hadoop bin/ directory to PATH\n', '# export PATH=$PATH:$HADOOP_HOME/bin:'+javah+'/bin\n', 'export PATH=$PATH:$HADOOP_HOME/bin\n', '\n']

        for line in flines:
                if '# Set Hadoop-related environment variables\n' in line:
                        print ' == .bashrc previously completed\n'
                        return

        f = open('/root/.bashrc','w')
        f.write(''.join(addinf+flines))
        f.close()
        print ' == Editing .bashrc completed'

print ' === Work with .bashrc Started'
print ' == '+wdir+'hadoop'
bashrc(wdir+'hadoop')

print ' === Work with .bashrc Complited'

