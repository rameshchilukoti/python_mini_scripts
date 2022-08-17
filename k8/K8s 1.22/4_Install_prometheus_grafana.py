import paramiko
import time
import re

from paramiko import sftp

username = "administrator"
password = "emclegato"

folder ="cd /home/administrator/prometheus_grafana"


def push_file_to_server(host, file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder, file)
    print("Uploading file from {} to {}".format(local_path,remote_path))
    s.put(local_path, remote_path)
    s.close()

fg = open('kworkers.txt')
for f in fg:

    host = f.rstrip()
    print("\033[1m" + host + "\033[0m")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)


    def execommand(thecommand):
        stdina, stdouta, stderra = client.exec_command(thecommand)
        print(thecommand)
        for i in stdouta.readlines():
            print("{}".format(i))
        for i in stderra.readlines():
            print('\x1b[1;31m' + i + '\x1b[0m')

        docker_list = "echo \"{}\" | sudo -S sudo docker image pull prom/prometheus; docker image pull prom/alertmanager;docker image pull grafana/grafana".format(password)
        print(docker_list)
        execommand(docker_list)
    client.close()
fg.close()
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

    #Push the necessary files to the server
    push_file_to_server(host, "clusterRole.yaml")
    push_file_to_server(host, "config-map.yaml")
    push_file_to_server(host, "deployment.yaml")
    push_file_to_server(host, "grafana-datasource-config.yaml")
    push_file_to_server(host, "prometheus-deployment.yaml")
    push_file_to_server(host, "prometheus-ingress.yaml")
    push_file_to_server(host, "prometheus-service.yaml")
    push_file_to_server(host, "service.yaml")

    execommand("kubectl create namespace monitoring")
    execommand("kubectl create -f clusterRole.yaml")
    execommand("kubectl create -f config-map.yaml")
    execommand("kubectl create  -f prometheus-deployment.yaml")
    execommand("kubectl get deployments --namespace=monitoring")
    execommand("kubectl get pods --namespace=monitoring")
    execommand("kubectl create -f prometheus-service.yaml --namespace=monitoring")
    execommand("kubectl create -f grafana-datasource-config.yaml")
    execommand("kubectl create -f deployment.yaml")
    execommand("kubectl create -f service.yaml")


    get_pods = "kubectl get pods -A"
    execommand(get_pods)
    print("Access prometheus at http://{}:30000 and grafana at http://{}:32000 with credentials admin/admin. Import "
          "Grafana dashboard id : 12740".format(host, host))

    client.close()
fh.close()



