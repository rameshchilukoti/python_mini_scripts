import paramiko
import re
username = "administrator"
password = "emclegato"
fh = open('k.txt')
for f in fh:
    host = f.rstrip()
    print("\033[1m" + host + "\033[0m")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)


    def execommand(thecommand):
        stdina, stdouta, stderra = client.exec_command(thecommand)
        print(thecommand)
        outputlist = []
        for i in stdouta.readlines():
            print("{}".format(i))
            outputlist.append(i)
        for i in stderra.readlines():
            print('\x1b[1;31m' + i + '\x1b[0m')
        return outputlist
    def printOutPut(list):
        for i in list:
            print(i)

    # get_ns = "kubectl get namespace | grep cproxy | awk '{print$1}'"
    get_ns = "kubectl get pod --all-namespaces | grep namespace- | grep \"CrashLoopBackOff\" | grep -v \"NAME\" | awk '{{print$1}}'"
    # get_ns = "kubectl get pods --all-namespaces | grep \"namespace-*\" | grep \"ContainerCreating\" | awk '{{print$1}}'"
    namespaces = execommand(get_ns)
    for ns in namespaces:
        type_of_deployment = ["pods","deployments","statefulsets.apps","pvc"]
        for type in type_of_deployment:
            # get_deployments = "kubectl get {} -n {} |grep \"CrashLoopBackOff\"| grep -v \"NAME\" | awk '{{print$1}}'".format(type.rstrip(), ns.rstrip())
            get_deployments = "kubectl get {} -n {} |grep \"0/1\" | awk '{{print$1}}'".format(type.rstrip(), ns.rstrip())
            apps = execommand(get_deployments)
            for app in apps:
                print("\033[1m" + "DELETE {} OF TYPE {} FROM NAMESPACE {}".format(app.rstrip(), type.rstrip(),ns.rstrip()) + "\033[0m")
                delete_deployments = "kubectl delete {} {} -n {} --force --grace-period 0".format(type.rstrip(), app.rstrip(), ns.rstrip())
                execommand(delete_deployments)
        # delete_ns = "kubectl delete namespace {}".format(ns)
        # execommand(delete_ns)
    # get_pv = "kubectl get pv | grep Released | awk '{print$1}'"
    # pvs = execommand(get_pv)
    # for pv in pvs:
    #     print("\033[1m" + "DELETE {}".format(pv) + "\033[0m")
    #     delete_pv = "kubectl delete pv {}".format(pv)
    #     execommand(delete_pv)

    client.close()
fh.close()