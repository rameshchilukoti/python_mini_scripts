import paramiko
import time
import re
username = "administrator"
password = "emclegato"
cluster_id = "demo-cluster-1zg"
# vc_ip = "10.98.49.50"
# datacenter = "Datacenter-50"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# vc_ip = "10.125.12.101"
# datacenter = "Datacenter_K8VMware"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
#
#
# vc_ip = "10.198.48.147"
# datacenter = "Datacenter-147"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
#Blended
# vc_ip = "10.198.184.74"
# datacenter = "Blended_VC"
# vc_username = "administrator@vsphere.local"
# vc_password = "Changeme@1"

# # CR
# vc_ip = "10.198.49.100"
# datacenter = "SIT"
# vc_username = "administrator@vsphere.local"
# vc_password = "Changeme@1"
# home = "/home/administrator"

# vc_ip = "10.198.48.141"
# datacenter = "Cyber_Recovery"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# # home = "/home/administrator"
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

#
# #MVLAN
# vc_ip = "10.198.51.170"
# datacenter = "PPDM"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# home = "/home/administrator"
#
# vc_ip = "10.226.79.99"
# datacenter = "Cyber_Recovery"
# vc_username = "administrator@vsphere.local"
# vc_password = "Emclegato@123"
# home = "/home/administrator"

i = 119
fh = open('kmasters.txt')
for f in fh:
    host = f.rstrip()
    print("\033[1m" + host + "\033[0m")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)

    i = i+1
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

    # print("CREATE CSI SECRET")
    # copy_csi_vsphere_conf = "cd /home/administrator;echo {} | sudo -S cp csi-vsphere.conf /etc/kubernetes/".format(password)
    # change_id ="cd /etc/kubernetes/;echo {} | sudo -S sed -i '0,/cluster-id = \"demo-cluster-id\"/s/cluster-id = \"demo-cluster-id\"/cluster-id = \"{}-{}\"/' csi-vsphere.conf".format(password,cluster_id,i)
    # change_vc ="cd /etc/kubernetes/;echo {} | sudo -S sed -i '0,/VirtualCenter \"10.125.12.101\"/s/VirtualCenter \"10.125.12.101\"/VirtualCenter \"{}\"/' csi-vsphere.conf".format(password, vc_ip)
    # change_vc_pswd = "cd /etc/kubernetes/;echo {} | sudo -S sed -i '0,/password = \"Emclegato@123\"/s/password = \"Emclegato@123\"/password = \"{}\"/' csi-vsphere.conf".format(password, vc_password)
    # change_datacenter ="cd /etc/kubernetes/;echo {} | sudo -S sed -i '0,/datacenters = \"VMDM\"/s/datacenters = \"VMDM\"/datacenters = \"{}\"/' csi-vsphere.conf".format(password, datacenter)
    # create_csi_secret = "cd /etc/kubernetes/;kubectl create secret generic vsphere-config-secret --from-file=csi-vsphere.conf --namespace=kube-system;cat csi-vsphere.conf "
    # execommand(copy_csi_vsphere_conf)
    # execommand(change_id)
    # time.sleep(75)
    # execommand(change_vc)
    # execommand(change_vc_pswd)
    # execommand(change_datacenter)
    # execommand(create_csi_secret)
    # print("GET CSI SECRET")
    # get_csi_secret = "kubectl get secret vsphere-config-secret --namespace=kube-system"
    # execommand(get_csi_secret)


    # print("CREATE ROLE SERVICE")
    # create_role_service = "wget https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/manifests/v1.0.2/rbac/vsphere-csi-controller-rbac.yaml;kubectl apply -f vsphere-csi-controller-rbac.yaml"   #https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/manifests/v1.0.2/rbac/
    # execommand(create_role_service)
    # #
    # print("CREATE VSPHERE_CSI_CONTROLLER_SS")
    # #1.02
    # # wget_controller_ss = "wget  https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/manifests/1.14/deploy/vsphere-csi-controller-ss.yaml"
    # apply_controller_ss = "kubectl apply -f vsphere-csi-controller-ss.yaml"

    # change_config_path = "cd /home/administrator;sed -i 's/value=\/etc\/cloud\/csi-vsphere.conf/val=\/etc\/kubernetes\/csi-vsphere.conf/g' vsphere-csi-controller-ss.yaml"
    # change_mount_path = "cd /home/administrator;sed -i 's/mountPath: \/etc\/cloud/mountPath: \/etc\/kubernetes/g' vsphere-csi-controller-ss.yaml"
    # # deploy_manifest1="kubectl apply -f vsphere-csi-controller-ss.yaml"
    # # #
    # # # execommand(wget_controller_ss)
    # # execommand(apply_controller_ss)
    # execommand(change_config_path)
    # execommand(change_mount_path)
    # # execommand(deploy_manifest1)
    # #
    # # print("CREATE VSPHERE CSI NODE")
    # # # wget_node_ss = "kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/manifests/1.14/deploy/vsphere-csi-node-ds.yaml"
    # # wget_node_ss = "kubectl apply -f vsphere-csi-node-ds.yaml"
    #
    # change_config_path2 = "cd /home/administrator;sed -i 's/--cloud-config=\/etc\/cloud\/csi-vsphere.conf/--cloud-config=\/etc\/kubernetes\/csi-vsphere.conf/g' vsphere-csi-node-ds.yaml"
    # change_mount_path2 = "cd /home/administrator;sed -i 's/mountPath: \/etc\/cloud/mountPath: \/etc\/kubernetes/g' vsphere-csi-node-ds.yaml"
    # # deploy_manifest2 = "kubectl apply -f vsphere-csi-node-ds.yaml"
    # # execommand(wget_node_ss)
    # execommand(change_config_path2)
    # execommand(change_mount_path2)
    # # execommand(deploy_manifest2)
    #
    # # executeversion2folderdelete = "kubectl delete -f version2csi/"
    # # executeversion2folder = "kubectl apply -f version2csi/"
    # # execommand(executeversion2folderdelete)
    # # execommand(executeversion2folder)
    #
    #
    # executeversion2folderdelete = "kubectl delete -f csi2.0/"
    # executeversion2folder = "kubectl apply -f csi2.0/"
    # execommand(executeversion2folderdelete)
    # execommand(executeversion2folder)
    # time.sleep(10)
    #
    # print("VERIFY")
    # verify1 = "kubectl get statefulset --namespace=kube-system"
    # verify2 = "kubectl get daemonsets vsphere-csi-node --namespace=kube-system"
    # verify3 = "kubectl get pods --namespace=kube-system"
    # verify4 = "kubectl get CSINode"
    # verify5 = "kubectl get csidrivers"
    # verify6 = "kubectl get nodes"
    # verify7 = "kubectl describe nodes | grep \"ProviderID\""
    # execommand(verify1)
    # execommand(verify2)
    # execommand(verify3)
    # execommand(verify4)
    # execommand(verify5)
    # execommand(verify6)
    # execommand(verify7)
    # print("#############################################")
    client.close()
fh.close()