import paramiko
import time
import re

from paramiko import sftp

username = "administrator"
password = "emclegato"

cpi_secret = "cpi-vmdm-secret"
folder ="cd /home/administrator"

# vc_ip = "10.98.49.50"
# datacenter = "Datacenter-50"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"


# vc_ip = "10.198.184.74"
# datacenter = "Blended_VC"
# vc_username = "administrator@vsphere.local"
# vc_password = "Changeme@1"
# home = "/home/administrator"

# vc_ip = "10.125.12.101"
# datacenter = "Datacenter_K8VMware"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# home = "/home/administrator"
#
# vc_ip = "10.198.48.147"
# datacenter = "Datacenter-147"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# home = "/home/administrator"

# #MVLAN
# vc_ip = "10.198.51.170"
# datacenter = "PPDM"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# home = "/home/administrator"

# # CR
# vc_ip = "10.198.49.100"
# datacenter = "SIT"
# vc_username = "administrator@vsphere.local"
# vc_password = "Changeme@1"
# home = "/home/administrator"
#
# vc_ip = "10.198.48.141"
# datacenter = "Cyber_Recovery"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# home = "/home/administrator"
#
#
# vc_ip = "10.198.49.100"
# datacenter = "SIT"
# vc_username = "administrator@vsphere.local"
# vc_password = "Changeme@1"
# home = "/home/administrator"



vc_ip = "10.226.79.73"
datacenter = "10.198.146_Series"
vc_username = "administrator@vsphere.local"
vc_password = "Changeme@123"
home = "/home/administrator"


# vc_ip = "10.226.79.99"
# datacenter = "Cyber_Recovery"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# home = "/home/administrator"

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

    #CPI config map
    copy_vsphere_conf = "cd {};echo {} | sudo -S cp vsphere.conf /etc/kubernetes/".format(home,password)
    change_vc ="cd /etc/kubernetes/;echo {} | sudo -S sed -i '0,/VirtualCenter \"10.125.12.101\"/s/VirtualCenter \"10.125.12.101\"/VirtualCenter \"{}\"/' vsphere.conf".format(password, vc_ip)
    change_datacenter ="cd /etc/kubernetes/;echo {} | sudo -S sed -i '0,/datacenters = \"VMDM\"/s/datacenters = \"VMDM\"/datacenters = \"{}\"/' vsphere.conf".format(password, datacenter)
    change_secret ="cd /etc/kubernetes/;echo {} | sudo -S sed -i '0,/secret-name = \"cpi-vmdm-secret\"/s/secret-name = \"cpi-vmdm-secret\"/secret-name = \"{}\"/' vsphere.conf".format(password, cpi_secret)
    create_config_map = "cd /etc/kubernetes/;kubectl create configmap cloud-config --from-file=vsphere.conf --namespace=kube-system"
    get_config_map = "kubectl get configmap cloud-config --namespace=kube-system"

    #CPI secret
    change_cpi_secret = "cd {};sed -i '0,/name: cpi-vmdm-secret/s/name: cpi-vmdm-secret/name: {}/' cpi-VMDM-secret.yml".format(home,cpi_secret)
    change_vc_ip = "cd {};sed -i 's/10.125.12.101/{}/g' cpi-VMDM-secret.yml".format(home,vc_ip)
    change_username = "cd {};sed -i '0,/administrator@vsphere.local/s/administrator@vsphere.local/{}/' cpi-VMDM-secret.yml".format(home,vc_username)
    change_pswd = "cd {};sed -i '0,/Emclegato@123/s/Emclegato@123/{}/' cpi-VMDM-secret.yml".format(home,vc_password)
    create_cpi_secret = "cd {};kubectl create -f cpi-VMDM-secret.yml".format(home)
    get_cpi_secret = "cd {};kubectl get secret {} --namespace=kube-system".format(home,cpi_secret)

    # CPI config map
    execommand(copy_vsphere_conf)
    execommand(change_vc)
    execommand(change_datacenter)
    execommand(change_secret)
    execommand(create_config_map)
    execommand(get_config_map)
    # CPI secret
    execommand(change_cpi_secret)
    execommand(change_vc_ip)
    execommand(change_username)
    execommand(change_pswd)
    execommand(create_cpi_secret)
    execommand(get_cpi_secret)

    get_taints = "kubectl describe nodes | egrep \"Taints:|Name:\""
    deploy_manifest1 = "wget https://raw.githubusercontent.com/kubernetes/cloud-provider-vsphere/master/manifests/controller-manager/cloud-controller-manager-roles.yaml;kubectl apply -f cloud-controller-manager-roles.yaml"
    deploy_manifest2 = "wget https://raw.githubusercontent.com/kubernetes/cloud-provider-vsphere/master/manifests/controller-manager/cloud-controller-manager-role-bindings.yaml;kubectl apply -f cloud-controller-manager-role-bindings.yaml"
    wget_manifest3 = "cd {};wget https://github.com/kubernetes/cloud-provider-vsphere/raw/master/manifests/controller-manager/vsphere-cloud-controller-manager-ds.yaml".format(home)
    change_config_path = "cd {};sed -i 's/--cloud-config=\/etc\/cloud\/vsphere.conf/--cloud-config=\/etc\/kubernetes\/vsphere.conf/g' vsphere-cloud-controller-manager-ds.yaml".format(home)
    change_mount_path = "cd {};sed -i 's/mountPath: \/etc\/cloud/mountPath: \/etc\/kubernetes/g' vsphere-cloud-controller-manager-ds.yaml".format(home)
    deploy_manifest3 = "kubectl apply -f vsphere-cloud-controller-manager-ds.yaml"
    time.sleep(20)
    verify_cpi = "kubectl get pods --namespace=kube-system"
    check_untaint = "kubectl describe nodes | egrep \"Taints:|Name:\""
    execommand(get_taints)
    #deploy cpi manifest
    execommand(deploy_manifest1)
    execommand(deploy_manifest2)
    execommand(wget_manifest3)
    execommand(change_config_path)
    execommand(change_mount_path)
    execommand(deploy_manifest3)
    time.sleep(1)
    #verify cpi

    execommand(verify_cpi)
    execommand(check_untaint)


    print("#############################################")
    client.close()
fh.close()