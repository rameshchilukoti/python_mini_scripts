import paramiko

username = "administrator"
password = "emclegato"
fh = open('kmasters.txt')
print("DELETE PPDM AND VELERO NAMESPACE, CRD's and CRB's FROM WORKERNODES")
# add master nodes ip in kmasters.txt and add worker node IP in kworkers.txt
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

    namespace_to_delete =["velero","powerprotect"]
    for namespace in namespace_to_delete:
        get_pods = "cd /home/administrator;kubectl get pod --namespace={} | grep {} | awk '{{print$1}}'".format(namespace,namespace)
        stdina, stdouta, stderra = client.exec_command(get_pods)
        for pod in stdouta.readlines():
            pod_name = pod.rstrip()
            delete_pod = "kubectl delete pod {} -n={}".format(pod_name,namespace)
            execommand(delete_pod)
    #delete powerprotect componenets
    delete_crd = "kubectl delete crd -l app.kubernetes.io/part-of=powerprotect.dell.com"
    delete_crb ="kubectl delete clusterrolebinding powerprotect:cluster-role-binding"
    delete_crb1 = "kubectl delete crd applicationtemplates.powerprotect.dell.com            "
    delete_crb2 = "kubectl delete crd backupjobs.powerprotect.dell.com                      "
    delete_crb3 = "kubectl delete crd backups.velero.io                                     "
    delete_crb4 = "kubectl delete crd backupstoragelocations.powerprotect.dell.com          "
    delete_crb5 = "kubectl delete crd backupstoragelocations.velero.io                      "
    delete_crb6 = "kubectl delete crd canceljobs.powerprotect.dell.com                      "
    delete_crb7 = "kubectl delete crd deletebackupjobs.powerprotect.dell.com                "
    delete_crb8 = "kubectl delete crd deletebackuprequests.velero.io                        "
    delete_crb9 = "kubectl delete crd downloadrequests.velero.io                            "
    delete_crb10 = "kubectl delete crd crdvolumebackups.velero.io                            "
    delete_crb11 = "kubectl delete crd crdvolumerestores.velero.io                           "
    delete_crb12 = "kubectl delete crd resticrepositories.velero.io                          "
    delete_crb13 = "kubectl delete crd restorejobs.powerprotect.dell.com                     "
    delete_crb14 = "kubectl delete crd restores.velero.io                                    "
    delete_crb15 = "kubectl delete crd schedules.velero.io                                   "
    delete_crb16 = "kubectl delete crd serverstatusrequests.velero.io                        "
    delete_crb17 = "kubectl delete crd volumesnapshotlocations.velero.io                     "
    delete_crb18 = "kubectl delete crd podvolumebackups.velero.io                            "
    delete_crb19 = "kubectl delete crd podvolumerestores.velero.io                           "
    delete_crb20 = "kubectl delete crd backuprepositories.backupdriver.cnsdp.vmware.com      "
    delete_crb21 = "kubectl delete crd backuprepositoryclaims.backupdriver.cnsdp.vmware.com  "
    delete_crb22 = "kubectl delete crd clonefromsnapshots.backupdriver.cnsdp.vmware.com      "
    delete_crb23 = "kubectl delete crd deletesnapshots.backupdriver.cnsdp.vmware.com         "
    delete_crb24 = "kubectl delete crd downloads.datamover.cnsdp.vmware.com                  "
    delete_crb25 = "kubectl delete crd snapshots.backupdriver.cnsdp.vmware.com               "
    delete_crb26 = "kubectl delete crd uploads.datamover.cnsdp.vmware.com                    "
    delete_crb27 = "kubectl delete crd -l app.kubernetes.io/part-of=powerprotect.dell.com    "
    delete_crb28 = "kubectl delete clusterrolebinding powerprotect:cluster-role-binding      "
    delete_ns = "kubectl delete namespace powerprotect"

    execommand(delete_crd)
    execommand(delete_crb)
    execommand(delete_crb1)
    execommand(delete_crb2)
    execommand(delete_crb3)
    execommand(delete_crb4)
    execommand(delete_crb5)
    execommand(delete_crb6)
    execommand(delete_crb7)
    execommand(delete_crb8)
    execommand(delete_crb9)
    execommand(delete_crb10)
    execommand(delete_crb11)
    execommand(delete_crb12)
    execommand(delete_crb13)
    execommand(delete_crb14)
    execommand(delete_crb15)
    execommand(delete_crb16)
    execommand(delete_crb17)
    execommand(delete_crb18)
    execommand(delete_crb19)
    execommand(delete_crb20)
    execommand(delete_crb21)
    execommand(delete_crb22)
    execommand(delete_crb23)
    execommand(delete_crb24)
    execommand(delete_crb25)
    execommand(delete_crb26)
    execommand(delete_crb27)
    execommand(delete_crb28)
    execommand(delete_ns)

    #delete velero components
    delete_crd_velero = "kubectl delete crd -l component=velero"
    delete_crb_velero = "kubectl delete clusterrolebinding velero"
    delete_ns_velero = "kubectl delete namespace velero-ppdm"

    execommand(delete_crd_velero)
    execommand(delete_crb_velero)
    execommand(delete_ns_velero)

    client.close()
fh.close()

fh = open('kworkers.txt')
print("DELETE PPDM AND VELERO IMAGES FROM WORKERNODES")

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
    namespace_to_delete =["velero", "powerprotect", "cproxy", "backup-driver", "ap-sc.drm"]
    for ns in namespace_to_delete:
        docker_list = "echo \"{}\" | sudo -S sudo docker image ls |grep {} | awk '{{print$3}}' ".format(password, ns)
        print(docker_list)
        stdina, stdouta, stderra = client.exec_command(docker_list)
        for images in stdouta.readlines():
            print(images.rstrip())
            remove_image = "echo \"{}\" | sudo -S sudo docker image remove {} --force".format(password, images.rstrip())
            execommand(remove_image)
    list_docker_images = "echo \"{}\" | sudo -S sudo docker image ls".format(password)
    execommand(list_docker_images)
client.close()
fh.close()

