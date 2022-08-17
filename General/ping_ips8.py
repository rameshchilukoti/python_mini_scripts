import paramiko
from colorama import Fore
import glob
import re
import os
username = "administrator"
password = "emclegato"
host = "10.198.184.202"
# range1 = "10.198.184."
# range1 = "10.198.49."
# range1 = "10.198.49."
# range1 = "10.198.50."
# range1 = "10.198.51."
# range1 = "10.198.52."
# range1 = "10.198.146."
# range1 = "10.198.185."
# range1 = "10.226.78."
range1 = "10.226.79."
# range1 = "10.226.34."
# range1 = "10.226.152."
# range1 = "10.125.12."





count =0
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
for j in range(2, 255):
    command = "ping -c 1 {}{}".format(range1,j)
    stdina, stdouta, stderra = client.exec_command(command)
    for i in stdouta.readlines():
        # print("{}".format(i))
        if re.search("64 bytes from", i):
            print("{}{} is in use".format(range1,j))
        if re.search("100% packet loss", i):
            print('\x1b[1;31m'+ "{}{} is NOT in use".format(range1,j)+ '\x1b[0m' )
            count=count+1
print("Total Free from range {}2 to {}255 is = {}".format(range1,range1,count))
client.close()
