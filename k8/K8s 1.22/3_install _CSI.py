import paramiko
import time
import re
import random
import string
from random import randint
import pysftp as sftp

username = "administrator"
password = "emclegato"
folder ="/home/administrator"

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


def randomString(stringLength=10):
   """Generate a random string of fixed length """
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(stringLength))


def random_with_N_digits(n):
   range_start = 10 ** (n - 1)
   range_end = (10 ** n) - 1
   return randint(range_start, range_end)



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

    print("GET ALL NODES")
    get_master_node = "kubectl describe nodes | egrep \"Name:\" | awk '{print $2}'"
    list = execommand(get_master_node)
    if(list.__len__() != 0):
        print(list[0].rstrip("\n"))


        print("CHECK FOR TAINT IN MASTER NODE")
        check_master_taint = "kubectl describe node {} | egrep \"Taints:\" | awk '{{print $2}}'".format(list[0].rstrip("\n"))
        output = execommand(check_master_taint)

        if re.search("master:NoSchedule",output[0]):
            print("TAINT IS PRESENT ON MASTER, GO AHEAD")
        else:
            print("TAINT NOT FOUND ON MASTER. ADDING TAINT")
            add_taint_master = "kubectl taint nodes {} node-role.kubernetes.io/master=:NoSchedule".format(output[0])
            execommand(add_taint_master)

    create_namespace="kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/v2.5.1/manifests/vanilla/namespace.yaml"
    execommand(create_namespace)

    push_file_to_server(host, "csi-vsphere.conf")

    change_id = "sed -i '0,/cluster-ids/s/cluster-ids/cluster-{}/' csi-vsphere.conf".format(randomString(4))
    print(change_id)
    change_vc = "sed -i '0,/10.226.79.73/s/10.226.79.73/{}/' csi-vsphere.conf".format(vc_ip)
    change_vc_pswd = "sed -i '0,/Changeme@123/s/Changeme@123/{}/' csi-vsphere.conf".format(vc_password)
    change_datacenter = "sed -i '0,/10.198.146_Series/s/10.198.146_Series/{}/' csi-vsphere.conf".format(datacenter)


    copy_csi_vsphere_conf = "cd /home/administrator;echo {} | sudo -S cp csi-vsphere.conf /etc/kubernetes/".format(password)



    create_csi_secret = "cd /etc/kubernetes/;kubectl create secret generic vsphere-config-secret --from-file=csi-vsphere.conf --namespace=vmware-system-csi;kubectl get secret vsphere-config-secret --namespace=vmware-system-csi;cat csi-vsphere.conf "

    apply_csi ="kubectl apply -f  https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/v2.5.1/manifests/vanilla/vsphere-csi-driver.yaml"


    execommand(change_id)
    execommand(change_vc)
    execommand(change_vc_pswd)
    execommand(change_datacenter)

    execommand(copy_csi_vsphere_conf)
    execommand(create_csi_secret)

    execommand(apply_csi)
    print("#############################################")

    print("VERIFY")
    verify1 = "kubectl get pods -A"
    verify3 = "kubectl get pods --namespace=kube-system"
    verify4 = "kubectl get CSINode"
    verify5 = "kubectl get csidrivers"
    verify6 = "kubectl get nodes"
    verify7 = "kubectl describe nodes | grep \"ProviderID\""
    execommand(verify1)
    execommand(verify3)
    execommand(verify4)
    execommand(verify5)
    execommand(verify6)
    execommand(verify7)
    print("#############################################")
    client.close()
fh.close()