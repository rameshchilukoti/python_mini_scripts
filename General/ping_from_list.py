import paramiko
from colorama import Fore
import glob
import re
import os
username = "administrator"
password = "emclegato"
host = "10.198.184.202"




count =0
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)

fh = open('ip.txt')
for f in fh:
    host = f.rstrip()
    command = "ping -c 1 {}".format(host)
    stdina, stdouta, stderra = client.exec_command(command)
    for i in stdouta.readlines():
        # print("{}".format(i))
        if re.search("64 bytes from", i):
            print("{} is in use".format(host))
        if re.search("100% packet loss", i):
            print('\x1b[1;31m'+ "{} is NOT in use".format(host)+ '\x1b[0m' )
            count=count+1
client.close()
