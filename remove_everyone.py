#!/usr/bin/python

import os
import sys
import subprocess
import getopt
import re

def run (cmd, force_run):
  if force_run == False:
    if test == True:
      print cmd
      return iter ("TEST")
    else:
      p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      return iter(p.stdout.readline, b'')
  else:
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def rm_everyone (file):
  FORCE = True
  NO_FORCE = False
  synthetic = False
  cmd = "/bin/ls -lend '" + file + "'"
  for line in run (cmd, FORCE):
    syn_search = re.search (r'SYNTHETIC ACL', line)
    if syn_search is not None:
      synthetic = True
    lf = line.split(":")
    ace_num = lf[0].lstrip()
    if ace_num.isdigit() == True:
      ace_f = lf[2].split()
      sid = ace_f[0]
      if sid == "S-1-1-0":
        print "ACE " + ace_num + " of "+ file + " has everyone set " 
        if synthetic == True:
          if skip_synth == True:
              print "   No action taken per -s flag"
          else:
            if unix_chmod == False:
              cmd = "chmod -a# " + ace_num + " '" + file + "'"
              run (cmd, NO_FORCE)
            else:
              cmd = "chmod o-r '" + file + "'"
              run (cmd, NO_FORCE)
              cmd = "chmod o-w '" + file + "'"
              run (cmd, NO_FORCE)
              cmd = "chmod o-x '" + file + "'"
              run (cmd, NO_FORCE)
        else:
          cmd = "chmod -a# " + ace_num + " '" + file + "'"
          run (cmd, NO_FORCE)


test = False
files_only = False
unix_chmod = False
skip_synth= False
optlist, args = getopt.getopt (sys.argv[1:], 'tFsu')
for o, a in optlist:
  if o == '-t':
    test = True
  if o == '-F':
    files_only = True
  if o == '-s':
    skip_synth = True
  if o == '-u':
    unix_chmod = True
for dirname, subdirList, filelist in os.walk (args[0]):
  print "In DIR: " + dirname
  if not subdirList and not filelist:
    if files_only == False:
      rm_everyone (dirname)
  for fname in filelist:
    if files_only == False:
      rm_everyone (dirname)  
    file = dirname + "/" + fname
    rm_everyone (file)

