import paramiko

username = "administrator"
password = "emclegato"
storageClass_name = "sc-common"

fh = open('kmasters.txt')
for f in fh:
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

    #Remove CSI
    delete_Sc = "kubectl delete sc sc-common"
    delete1 ="kubectl delete -f vsphere-csi-node-ds.yaml"
    # delete1 = "kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/manifests/1.14/deploy/vsphere-csi-node-ds.yaml"
    delete2 ="kubectl delete -f vsphere-csi-controller-ss.yaml"
    # delete2 ="kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/manifests/1.14/deploy/vsphere-csi-controller-ss.yaml"
    delete3 ="kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/manifests/v1.0.2/rbac/vsphere-csi-controller-rbac.yaml"
    delete4 ="kubectl delete secret vsphere-config-secret --namespace=kube-system"
    delete5 ="kubectl get CSINode | grep -v \"NAME\"  | awk '{{print$1}}'"
    execommand(delete_Sc)
    execommand(delete1)
    execommand(delete2)
    execommand(delete3)
    execommand(delete4)
    execommand(delete5)
    stdina, stdouta, stderra = client.exec_command(delete5)
    for csiNode in stdouta.readlines():
        delete_node = "kubectl delete CSINode {}".format(csiNode)
        execommand(delete_node)

    #Remove CPI

    delete6 = "kubectl delete -f vsphere-cloud-controller-manager-ds.yaml"
    delete7 = "kubectl delete -f https://raw.githubusercontent.com/kubernetes/cloud-provider-vsphere/master/manifests/controller-manager/cloud-controller-manager-role-bindings.yaml"
    delete8 = "kubectl delete -f https://raw.githubusercontent.com/kubernetes/cloud-provider-vsphere/master/manifests/controller-manager/cloud-controller-manager-roles.yaml"
    delete9 = "kubectl delete secret cpi-vmdm-secret --namespace=kube-system"
    delete10 = "kubectl delete configmap cloud-config --namespace=kube-system"
    delete11 = "kubectl delete secret vsphere-config-secret --namespace=kube-system"
    execommand(delete6)
    execommand(delete7)
    execommand(delete8)
    execommand(delete9)
    execommand(delete10)
    execommand(delete11)
    executeversion2folderdelete = "kubectl delete -f csi2.0/"
    execommand(executeversion2folderdelete)
    # mv = "mkdir old;mv *.yml *.yaml old/"
    # execommand(mv)

    client.close()
fh.close()