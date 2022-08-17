import paramiko
import time
import re
username = "administrator"
password = "emclegato"
storageClass_name = "sc-common"


fh = open('kmasters.txt')
for f in fh:
    host = f.rstrip()

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


    get_ns ="kubectl get ns | grep namespace | awk '{{print$1}}'"
    stdina, stdouta, stderra = client.exec_command(get_ns)

    get_pod = "kubectl get pods --all-namespaces | grep \"namespace-*\" | nl"
    execommand(get_pod)

    get_pvc = "kubectl get pvc --all-namespaces | grep \"namespace-*\" | nl"
    execommand(get_pvc)

    print("#############################################")
    client.close()
fh.close()