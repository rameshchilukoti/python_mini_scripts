import pysftp as sftp
import paramiko
import time

username = "administrator"
password = "Changeme@1"      # Change into your Kuberenets master password
folder = "/home/administrator/automation"
client = paramiko.SSHClient()

def getClient(host):
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    return client

def execommand(client,thecommand):
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

def pull_file_from_server(host,file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder,file)
    print("Downloading file from {} to {}".format(remote_path,local_path))
    s.get(remote_path, local_path)
    s.close()

def edit_local_file(file):
    with open("foo.txt", "r+") as f:
        old = f.read()  # read everything in the file
        f.seek(0)  # rewind
        f.write("new line\n" + old)  # write the new line before


def push_file_to_server(host, file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder, file)
    print("Uploading file from {} to {}".format(local_path,remote_path))
    s.put(local_path, remote_path)
    s.close()

fh = open('kmasters.txt')
for f in fh:
    host = f.rstrip()
    print("\033[1m" + host + "\033[0m")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)


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


    #root user
    push_file_to_server(host, "resolv.conf")
    coomand1 = "echo \"Changeme@1\" | sudo -S cp /home/administrator/automation/resolv.conf /etc/resolv.conf"
    command2 = "echo \"Changeme@1\" | sudo -S docker login -u=chilur -p=Ram$india1"
    command3 = "echo \"Changeme@1\" | sudo -S sed -i '/10.226.79.9/d' /etc/hosts"
    command4 = "cat /etc/resolv.conf;cat /etc/hosts;cat /root/.docker/config.json"
    execommand(coomand1)
    execommand(command2)
    execommand(command3)
    execommand(command4)
    client.close()

