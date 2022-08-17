#README
#
import paramiko
import pysftp as sftp
import time
import re
username = "administrator"
password = "emclegato"
storageClass_name = "sc-common"
folder = "/home/administrator/automation"


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
    push_file_to_server(host, "cassandra-service.yaml")
    push_file_to_server(host, "cassandra-statefulset.yaml")
    push_file_to_server(host, "daemon.json")
    push_file_to_server(host, "deployment-postgres.yaml")
    push_file_to_server(host, "global-storageclass.yml")
    push_file_to_server(host, "mongodb-service.yaml")
    push_file_to_server(host, "mongodb-statefulset.yaml")
    push_file_to_server(host, "Mysql_Deployment.yaml")
    push_file_to_server(host, "MySql-pvc.yaml")
    push_file_to_server(host, "namespace.yaml")
    push_file_to_server(host, "PostgreSQL-pvc.yaml")
    push_file_to_server(host, "secret-postgres_NoNamespace.yaml")


    print("Change SC name")
    # mkdir = "mkdir {}; wget --no-check-certificate ".format(folder)
    change_sc = "cd {};grep -rli 'sc-common' * | xargs -i@ sed -i 's/sc-common/{}/g' @".format(folder,storageClass_name)
    #create Storage class
    create_sc = "cd {}; kubectl apply -f global-storageclass.yml".format(folder)
    #Get strorage class
    get_storage_class = "cd {};kubectl get storageclass {}".format(folder,storageClass_name)
    # execommand(change_sc)
    # execommand(create_sc)
    # execommand(get_storage_class)
    # execommand("kubectl get nodes;kubectl get pods --namespace=kube-system")
    # execommand("cd /home/administrator/automation/; cat PostgreSQL-pvc.yaml;cat PostgreSQL-pvc.yaml;cat MySql-pvc.yaml;cat Mysql_Deployment.yaml")

    print("#############################################")
    client.close()
fh.close()