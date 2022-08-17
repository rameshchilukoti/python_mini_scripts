import paramiko
import time
import re

import pysftp as sftp
username = "administrator"
password = "emclegato"

cpi_secret = "cpi-vmdm-secret"
folder ="/home/administrator"
#
# vc_ip = "10.226.79.73"
# datacenter = "10.198.146_Series"
# vc_username = "administrator@vsphere.local"
# vc_password = "Changeme@123"
# home = "/home/administrator"


vc_ip = "10.226.152.228"
datacenter = "CNDM"
vc_username = "administrator@vsphere.local"
vc_password = "Changeme@123"
home = "/home/administrator"


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

    get_master_node = "kubectl describe nodes | egrep \"Name:\" | awk '{print $2}'"
    list = execommand(get_master_node)
    if (list.__len__() != 0):
        print("1")
        print(list[0].rstrip("\n"))

        print("CHECK FOR TAINT IN MASTER NODE")
        for i in list:
            check_taint = "kubectl describe node {} | egrep \"Taints:\" | awk '{{print $2}}'".format(i.rstrip("\n"))
            output = execommand(check_taint)
            add_taint_master = "kubectl taint node {} node.cloudprovider.kubernetes.io/uninitialized=true:NoSchedule".format(i.rstrip("\n"))
            execommand(add_taint_master)

    push_file_to_server(host, "vsphere-cloud-controller-manager.yaml")
    change_vc_ip = "sed -i 's/10.226.79.73/{}/g' vsphere-cloud-controller-manager.yaml".format( vc_ip)
    change_vc_user = "sed -i 's/administrator@vsphere.local/{}/g' vsphere-cloud-controller-manager.yaml".format( vc_username)
    change_vc_password = "sed -i 's/Changeme@123/{}/g' vsphere-cloud-controller-manager.yaml".format( vc_password)
    change_vc_datacenter = "sed -i 's/10.198.146_Series/{}/g' vsphere-cloud-controller-manager.yaml".format( datacenter)

    execommand(change_vc_ip)
    execommand(change_vc_user)
    execommand(change_vc_password)
    execommand(change_vc_datacenter)

    apply_cpi = "kubectl apply -f vsphere-cloud-controller-manager.yaml"
    execommand(apply_cpi)
    time.sleep(10)
    get_pods = "kubectl get pods -A"
    execommand(get_pods)

    client.close()
fh.close()