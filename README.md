sfromcvm
========

files and scripts from CernVM(master stratuslab)

hainstall.py - installation file hadoop hdfs in single-node mode


gen.py - script of generating files of the specified size 
Problem: File size must be specified in the script [didn't have time to finish!]
"count=<SIZE_OF_FILE>"


loadfile.py - script of downloading files in hdfs from local dir (on master)
look how many files in a directory - maximum number of threads
Problem: 
 - specify dir where files take "fdir ="
 - specify dir to put the files "ptdir ="
 - in the formula for calculating speed, you must specify the size of downloadable files "aggregated_write_rate += <SIZE_OF_FILE_IN_MB> / elem"



read20filesobo.py - script of downloading files from hdfs to local dir (on master)
BigProblem: need to know the names of the files "lfname = []" 

Problem: 
 - need to know the names dir (and dirs) in hdfs