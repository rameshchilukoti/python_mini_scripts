#README
#
import paramiko
import pysftp as sftp
import time
import re
username = "administrator"
password = "emclegato"
storageClass_name = "sc-common"
folder = "/home/administrator/dataload"

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


    def push_file_to_server(host, file):
        cnopts = sftp.CnOpts()
        cnopts.hostkeys = None
        s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
        local_path = file
        remote_path = "{}/{}".format(folder, file)
        print("Uploading file from {} to {}".format(local_path, remote_path))
        s.put(local_path, remote_path)
        s.close()


    mkdir = "mkdir {}".format(folder)
    execommand(mkdir)

    push_file_to_server(host, "posgres_data_load.sh")
    push_file_to_server(host, "Runinside_Postgres.sh")
    push_file_to_server(host, "get_DB_size_POSTGRES.sh")
    push_file_to_server(host, "Posgres_get_DB_size.sh")

    execommand("cd {};sh posgres_data_load.sh ".format(folder))
    execommand("cd {}; sh get_DB_size_POSTGRES.sh".format(folder))

    print("#############################################")
    client.close()
fh.close()