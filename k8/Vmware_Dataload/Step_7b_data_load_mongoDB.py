import paramiko
import time
import re
from pymongo import MongoClient
import logging
from faker import Factory
no_of_namespaces = "5"
username = "administrator"
password = "emclegato"
storageClass_name = "sc-common"
directory = "mongodb_dataload"#create a new directory
mongo_db_admin = "theadmin"    #db admin username
mongo_db_password = "emclegato"  #db admin password
json_file_name = "16mb.json"
no_of_DB = "1" #each db of size 16*64 MB = 1GB
no_of_collection = "64"  # each collection of size 16mb


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
    print("MongoDb dataloading")

    for ns in range(1, int(no_of_namespaces) + 1):
        get_pods = "cd /home/administrator/{};kubectl get pod --namespace=namespace-{} | grep mongo | awk '{{print$1}}'".format(
            directory, ns)
        stdina, stdouta, stderra = client.exec_command(get_pods)
        pod_list = stdouta.readlines()
        pod_0 = pod_list[0].rstrip()
        for db in range(1,int(no_of_DB)+1):
            for col in range(1, int(no_of_collection) + 1):
                mongo_import = "mongoimport --db gen{} --collection form{} --authenticationDatabase admin --username {} --password {} --file /tmp/{} --jsonArray".format(db,col,mongo_db_admin,mongo_db_password,json_file_name)
                kubectl_cp = "kubectl cp /home/administrator/dataload/{} --namespace=namespace-{} {}:/tmp/".format(json_file_name, ns, pod_0)
                kubectl_exec = "kubectl exec -it {} --namespace=namespace-{} -- bash -c \"{}\"".format(pod_0,ns,mongo_import)
                execommand(kubectl_cp)
                execommand(kubectl_exec)
    client.close()
fh.close()
