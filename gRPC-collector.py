/*

The script uses existing JTIMON collector(https://github.com/Juniper/jtimon) binary and enables always-on collector mode 
i.e when IP table counter for the TCP session does not increment every 60s, then the PID is restarted. This enables the script to re-connect telemetry connection on
router reboots.

172-master-snmpfree.json is the sensor profile in json format.

{
	"host": "172.19.64.102",
	"port": 50051,
	"influx": {
		"server": "127.0.0.1",
		"port": 8086,
		"dbname": "Juniper",
		"user": "influx",
		"password": "influxdb",
		"recreate": true,
		"measurement": "OC"
	},
	"paths": [{
		"path": "/interfaces",
		"freq": 2000
	}]
}

*/

#!/usr/bin/env python
import os
import time
import subprocess
import sys
import random
import string
if len(sys.argv) == 1:
    print "***Usage: ./ocst.py <IP>"
    sys.exit()
try:
    print "***Creating config JSON files..."
    alnum = string.ascii_letters + string.digits
    an = ""
    for i in range(5):
        an = an + random.choice(alnum)
        #print an
    #s = open("172-master-snmpfree-clrtxt.json").read()
    s = open("172-master-snmpfree.json").read()
    s = s.replace('DUT', sys.argv[1])
    s = s.replace('ID', sys.argv[1] + an)
    f = open(sys.argv[1] + '.json', 'w')
    f.write(s)
    f.close()
    print "***Creating WAN delays of 100ms..."
    os.system("echo \'lab1234\' | sudo -S tc qdisc del dev ens3f0 root")
    os.system("echo \'lab1234\' | sudo -S tc qdisc add dev ens3f0 root netem delay 100ms")
    os.system("echo \'lab1234\' | sudo -S tc -s qdisc ls dev ens3f0")
    print "***Killing old sessions..."
    os.system("echo \'lab1234\' | sudo -S kill -9 $(ps -aux | grep " + sys.argv[1] + ".json | grep -v sudo | grep -v grep | awk {\'print $2\'})")
    time.sleep(2)
    os.system("echo \'lab1234\' | sudo -S kill -9 $(ps -aux | grep " + sys.argv[1] + ".json | grep -v sudo | grep -v grep | awk {\'print $2\'})")
    time.sleep(2)
    os.system("echo \'lab1234\' | sudo -S kill -9 $(ps -aux | grep " + sys.argv[1] + ".json | grep -v sudo | grep -v grep | awk {\'print $2\'})")
    print "***Starting new sessions..."
    os.system('rm -rf ' + sys.argv[1] + '.log')
    os.system('rm -rf ./jtimon-linux-amd64-' + sys.argv[1])
    os.system('cp jtimon-linux-amd64 jtimon-linux-amd64-'+sys.argv[1])
    #os.system('echo \'lab1234\' | sudo -S nohup ./jtimon-linux-amd64-'+sys.argv[1]+ ' --config ' + sys.argv[1] + '.json  --log /home/ashwinak/grpc/gtc/log/' + sys.argv[1] + '.log &')
    #Don't write to file for lab1.
    os.system('echo \'lab1234\' | sudo -S iptables -D INPUT -p tcp --sport 10162 -s ' + sys.argv[1])
    os.system('echo \'lab1234\' | sudo -S iptables -A INPUT -p tcp --sport 10162 -s ' +sys.argv[1])
    os.system('echo \'lab1234\' | sudo -S nohup ./jtimon-linux-amd64-' +sys.argv[1]+ ' --config ' + sys.argv[1] + '.json &')
    while True:
        #check_pid = str('ps -aF | grep -v grep | grep -v sudo | grep ' + sys.argv[1] + str('.json') + str(" | awk {'print $2'}"))
        #status = subprocess.Popen('%s' % check_pid, shell=True, stdout=subprocess.PIPE).communicate()[0]
        #to clear iptable counters
        #os.system('sudo iptables -L INPUT -vxnZ')
        check_stat1 = 'echo \'lab1234\' | sudo -S iptables -L INPUT -vxn | grep ' +sys.argv[1] + '| awk {\'print $1\'}'
        stat1 = subprocess.Popen('%s' % check_stat1, shell=True, stdout=subprocess.PIPE).communicate()[0]
        stat1=stat1.strip()
        time.sleep(60)
        check_stat2 = 'echo \'lab1234\' | sudo -S iptables -L INPUT -vxn | grep ' + sys.argv[1] + '| awk {\'print $1\'}'
        stat2 = subprocess.Popen('%s' % check_stat2, shell=True, stdout=subprocess.PIPE).communicate()[0]
        stat2 = stat2.strip()
        if stat2 != stat1:
            print "***Session already active,do nothing,Printing Active sessions.."
            os.system("ps -aux | grep " + sys.argv[1] + str(".json | grep -v grep"))
        else:
            print "***Restarting sessions"
            os.system("echo \'lab1234\' | sudo -S kill -9 $(ps -aux | grep " + sys.argv[1] + ".json | grep -v sudo | grep -v grep | awk {\'print $2\'})")
            os.system("echo \'lab1234\' | sudo -S kill -9 $(ps -aux | grep " + sys.argv[1] + ".json | grep -v sudo | grep -v grep | awk {\'print $2\'})")
            time.sleep(2)
            os.system("echo \'lab1234\' | sudo -S kill -9 $(ps -aux | grep " + sys.argv[1] + ".json | grep -v sudo | grep -v grep | awk {\'print $2\'})")
            os.system("echo \'lab1234\' | sudo -S kill -9 $(ps -aux | grep " + sys.argv[1] + ".json | grep -v sudo | grep -v grep | awk {\'print $2\'})")
            os.system('echo \'lab1234\' | sudo -S iptables -L INPUT -vxnZ')
            #os.system('echo \'lab1234\' | sudo -S nohup ./jtimon-linux-amd64-' + sys.argv[1] + ' --config ' + sys.argv[1] + '.json  --log /home/ashwinak/grpc/gtc/log/' + sys.argv[1] + '.log &')
            #Don't write to file for lab1.
            os.system('echo \'lab1234\' | sudo -S nohup ./jtimon-linux-amd64-' + sys.argv[1] + ' --config ' + sys.argv[1] + '.json &')
            print "***Printing active sessions..."
            os.system("ps -aux | grep " +sys.argv[1]+ str(".json | grep -v grep"))
            time.sleep(60)
except KeyboardInterrupt:
    print "***Flushing IPtable rules"
    os.system('echo \'lab1234\' | sudo -S iptables -D INPUT -p tcp --sport 10162 -s ' + sys.argv[1])
    print "***User interrupted"
