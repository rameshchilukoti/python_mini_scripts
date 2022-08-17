import paramiko
from colorama import Fore
import glob
import re
import os
from paramiko import sftp

#####   For multiple hosts :   List of IPs of hosts to be connected stored in a text file
##### Eg:
##### 10.198.49.100
##### 10.198.49.101

fh = open('Ip_List.txt')
for f in fh:
    host = f.rstrip()
    print("\033[1m" + host + "\033[0m")


########    OR  for a single connection
######## specify the IP in variable "host"

host = "10.198.184.202"
username = "administrator"
password = "emclegato"


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)

######### To establish an ssh connection and execute commands
def execommand(thecommand):
    output = []
    stdina, stdouta, stderra = client.exec_command(thecommand)
    print(thecommand)
    for i in stdouta.readlines():
        print("{}".format(i))
        output.append(i)
    for i in stderra.readlines():
        print('\x1b[1;31m' + i + '\x1b[0m')
    return output


def printOutPut(list):
    for i in list:
        print(i)


command = " ls -"
list = execommand(command)
printOutPut(list)

client.close()


#---------------------------------------------------------------------------------------------------------



#### Funtion defintion
#### To push a file to destination server from the current directory of this script
folder = "/home"       ## directory path in destination server
def push_file_to_server(host, file):
        cnopts = sftp.CnOpts()
        cnopts.hostkeys = None
        s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
        local_path = file
        remote_path = "{}/{}".format(folder, file)
        print("Uploading file from {} to {}".format(local_path, remote_path))
        s.put(local_path, remote_path)
        s.close()

#### Function call
push_file_to_server(host,"any_file_name.txt")




#---------------------------------------------------------------------------------------------------------




#### Funtion defintion
#### To pull a file to the current directory of this script from a remote server
folder = "/home"       ## directory path in destination server
def pull_file_from_server(host,file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder,file)
    print("Downloading file from {} to {}".format(remote_path,local_path))
    s.get(remote_path, local_path)
    s.close()

#### Function call
pull_file_from_server(host, "discovery.yaml")





#---------------------------------------------------------------------------------------------------------




#### To edit a local file

def edit_local_file(file):
    with open("foo.txt", "r+") as f:
        old = f.read()  # read everything in the file
        f.seek(0)  # rewind
        f.write("new line\n" + old)  # write the new line before

