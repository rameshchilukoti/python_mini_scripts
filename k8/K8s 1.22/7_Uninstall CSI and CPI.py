import paramiko
import time
import re

import pysftp as sftp
username = "administrator"
password = "emclegato"

cpi_secret = "cpi-vmdm-secret"
folder ="/home/administrator"

def push_file_to_server(host, file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder, file)
    print("Uploading file from {} to {}".format(local_path, remote_path))
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


    delete_Sc = "kubectl delete sc sc-common"
    execommand(delete_Sc)
    delete_csi ="kubectl delete -f  https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/v2.5.1/manifests/vanilla/vsphere-csi-driver.yaml"
    execommand(delete_csi)
    delete_secret  = "rm -rf csi-vsphere.conf; cd /etc/kubernetes/;kubectl delete secret vsphere-config-secret --namespace=vmware-system-csi;rm -rf csi-vsphere.conf "
    execommand(delete_secret)
    delete_namespace="kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/v2.5.1/manifests/vanilla/namespace.yaml"
    execommand(delete_namespace)
    get_master_node = "kubectl describe nodes | egrep \"Name:\" | awk '{print $2}'"
    delete_cpi = "kubectl delete -f vsphere-cloud-controller-manager.yaml"
    execommand(delete_cpi)
    time.sleep(5)

    get_pods = "kubectl get pods -A"
    execommand(get_pods)

    client.close()
fh.close()