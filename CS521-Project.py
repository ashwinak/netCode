#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 00:51:38 2019
@author: ashwinak

Objective: The code below takes an offline CSV file as input with keys,value store and writes it to influxDB which will be later consumed by grafana for plotting graphs 
for router interface statistics. This code can be expanded to take live data from a router via streaming telemetry and plot graphs using grafana.

"""

try:
    import csv
    import pandas as pd
    from influxdb import InfluxDBClient
    from datetime import datetime
    import time
    import sys
    import subprocess

    
    class writeToInfluxDB:
        def __init__ (self,hostname):
            self.__ = self
            self.__hostname = hostname
        
        def setPoints(self,counterName,fileName):
            '''
            Pass any "counter name" and filename in CSV format like (interface-name,counter)
            
            '''
            client = InfluxDBClient(host='localhost', port=8086)
            client.switch_database('CS521')
            timestamp =  int(datetime.today().strftime('%s%f')) * 1000
            timestamp = timestamp - 3985000000
            for k,v in dict_ae_members.items():
            #print(dict_ae_members)
                l=0
                while l <len(v):
                    #print(k,v[l])
                    with open(fileName) as csv_file:
                        reader = csv.reader(csv_file,delimiter=',')
                        for row in reader:
                            for column in row:
                                if column == v[l]:
    #                                timestamp = timestamp + 9999999000
                                    timestamp = timestamp + 9999999999
    #                                print("format",timestamp)
                                    json_body = [
                                        {
                                            "measurement": "Traffic_stats",
                                            "tags": {
                                                    "Interface": column,
                                                    "Host": self.__hostname
                                            },
                                                    "time": timestamp,
                                                    "fields": {
                                                            counterName: int(row[1]),
                                                    }
                                        }
                                    ]        
                                    client.write_points(json_body)
                                    
                    l+=1

        def CSVtoDICT(self,CSV):
            '''
            Pass CSV file to map it to a dictionary.
            
            '''
            with open (CSV) as f:
                d=dict(filter(None,csv.reader(f)))
            return d
        
        def findAndReplace(self,in_file,find,replace):
            '''
            To Find and replace text in a file. 
            arg : input-file,find,replace
            '''
            with open (in_file, 'r') as f:
                file=f.read()
                while find in file:
                    file = file.replace(find,replace)
            with open(in_file, "w") as f:
                f.write(file)
            return file
        
        def filterContent(self,in_file,string,out_file):
            '''
            To filter contents from a file. 
            arg : input-file,searchString,outputfile
            '''
            with open (in_file) as iFile,open(out_file, 'w') as oFile:
                for line in iFile:
                    if (string in line):
                        oFile.write(line)
                    else:
                        continue
            return oFile
        
    ### Code execution starts here #####
    
    ###Check if influxdb is running
    
    status = subprocess.check_output("ps -ax | grep influxdb.conf | grep -v grep | awk {'print $4'}",shell=True).decode('ascii')
    if status.strip() != 'influxd':
        sys.exit()
    
    in_file = input("Enter the raw telemetry CSV log file with 2 columns  of format (key,value): ")
    
    with open('bad_lines.txt', 'w') as fp:
        sys.stderr = fp
        df = pd.read_csv(in_file,error_bad_lines=False)
        df.empty
    
    keywords = ["name","high-speed","-pkts", "-octets"]
    with open(in_file) as iFile, open('stats1.txt', 'w') as oFile:
        for line in iFile:
            if any(match in line for match in keywords):
                oFile.write(line)    
    
    #### Influxdb initialization
    client = InfluxDBClient(host='localhost', port=8086)
    client.drop_database('CS521')
    client.create_database('CS521')
    
    ##Instantiate one class instance per router.
    A = writeToInfluxDB('R1')
    #print(A.setPoints.__doc__)
    #print(A.CSVtoDICT.__doc__)
    #print(A.filterContent.__doc__)
    #print(A.findAndReplace.__doc__)
            
    A.filterContent('stats1.txt','parent_ae_name, ae','parent_ae_name.csv')
    
    A.findAndReplace('parent_ae_name.csv',"interfaces/interface/", '')
    A.findAndReplace('parent_ae_name.csv',"/state/parent_ae_name", '')
    A.findAndReplace('parent_ae_name.csv'," ", '')
    dict_parent_ae_name = {}
    dict_parent_ae_name = A.CSVtoDICT('parent_ae_name.csv')
    #print(dict_parent_ae_name)
    set2=set()
    for k,v in dict_parent_ae_name.items():
        set2.add(v)
    #print(set2)
    list_ae_names = list(set2)
    #print(list_ae_names)
    dict_ae_members = {}
    
    i=0
    while i <len(list_ae_names):
        ae = list_ae_names[i]
        dict_ae_members['list_%s' % ae] = []
        i+=1
        
        
    for k,v in dict_parent_ae_name.items():
        i=0
        while i < len(list_ae_names):
            if list_ae_names[i] == v:
                #print (list_ae_names[i],":",k)
                ae = list_ae_names[i]
                dict_ae_members['list_%s' % ae].append(k)
            i+=1
    #print(dict_ae_members)
    
    graphs = []
    graphs = ['in-pkts','out-pkts','in-octets','out-octets','in-unicast-pkts','out-unicast-pkts','in-multicast-pkts','out-multicast-pkts']
    
    print("Writing data to influxdb...")
    t1 = round(time.time())
    for kw in graphs:
        file = kw + '.csv'
        counter = "/state/counters/" + kw
        A.filterContent('stats1.txt',kw,file)
        A.findAndReplace(file,"interfaces/interface/", '')
        A.findAndReplace(file,counter, '')
        A.findAndReplace(file," ", '')   
        A.setPoints(kw,file)
    print("")    
    print("Writing data to influxdb Complete.")
    t2 = round(time.time())
    delay = t2 - t1
    print("Time taken to write data to influxdb is,",delay,"seconds")


except (ImportError,NameError):
        print("")
        print("%%% Usage: python3 main.py")
        print("")
        print('''%%%%   Influxdb,Pandas or some other module is not installed ,check readme.md for more details. %%%%
        
        To install and run influxdb for python, follow this link

        https://www.influxdata.com/blog/getting-started-python-influxdb/

        To install influxdb, use this command:

        $ python3 -m pip install influxdb
        
        To install pandas, use this command:
        
        $ pip3 install pandas
            ''')
    
except KeyboardInterrupt:
    print("")
    print("User interrupted")

except FileNotFoundError:
    print("")
    print("The file",in_file, "is not found from the location you are running this code")
    print("")

except pd.errors.EmptyDataError:
    print("")    
    print("The file",in_file, "is empty")
    print("")
        
except pd.errors.ParserError:
    print("")    
    print("The file",in_file, "is not in CSV format i.e. there is a parser error")
    print("")

except SystemExit:
        print("")
        print(''' %%%%   Influxdb is not running,check readme.md for more details. %%%%
        
        To run influxdb for python, follow this link

        https://www.influxdata.com/blog/getting-started-python-influxdb/

        After installation, run this command from a terminal before executing this code

        $ influxd -config /usr/local/etc/influxdb.conf
            ''')

##comment the below code if errors are seen after proper influxdb installation.

except Exception as e:
    print("")
    print("Printing the exception for further debugging...")
    print(e)
    
except:
    print("")
    print("General error!!Comment this piece of code to debug further.")
    print("")            

