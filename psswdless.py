#! /usr/bin/env python
import sys
import os
import subprocess
if len(sys.argv) < 3:
    print ("Usage python psswdless.py <remote ip> <uname>")
    sys.exit()
else:
    key=os.system("ls -lrt ~/.ssh/id_rsa.pub")
    if key == 0:
        print ("###Public key already exist")
    else:
        os.system('ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""')

print ("Remote host is %s...." %sys.argv[1])
print ("Finding home directory in remote host...")
#home_dir = str(os.system('ssh -o StrictHostKeyChecking=no ' + sys.argv[2] + '@' + sys.argv[1] + " \'echo $HOME\'"))
home_dir = subprocess.check_output('ssh -o StrictHostKeyChecking=no ' + sys.argv[2] + '@' + sys.argv[1] + " \'echo $HOME\'", shell=True).decode('ascii').strip()
print ("Remote home directory is ",home_dir)
print ("Creating remote ssh directory...")
print('ssh -o StrictHostKeyChecking=no ' + sys.argv[2] + '@' + sys.argv[1] + ' mkdir -p ' +home_dir+ '/.ssh')
os.system('ssh -o StrictHostKeyChecking=no ' + sys.argv[2] + '@' + sys.argv[1] + ' mkdir -p ' +home_dir+ '/.ssh')
print ("Copying local pub key to remote home_dir/.ssh/authorized_keys")
#print("cat ~/.ssh/id_rsa.pub |ssh "  + sys.argv[2] + '@' + sys.argv[1] + " cat >> " + home_dir + "/.ssh/authorized_keys")
os.system("cat ~/.ssh/id_rsa.pub |ssh "  + sys.argv[2] + '@' + sys.argv[1] + " \'cat >> " + home_dir + "/.ssh/authorized_keys\'")
print ("Changing permissions for remote ~/.ssh/authorized_keys")
#print('ssh ' + sys.argv[2] +'@' + sys.argv[1] + " chmod 700 .ssh; chmod 640 " +home_dir+ "/.ssh/authorized_keys")
os.system('ssh ' + sys.argv[2] +'@' + sys.argv[1] + " \'chmod 700 .ssh; chmod 640 " +home_dir+ "/.ssh/authorized_keys\'")
