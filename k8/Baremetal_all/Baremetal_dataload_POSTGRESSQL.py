import paramiko
import time
import re
username = "administrator"
password = "emclegato"
no_of_namespaces = "10"

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

    for ns in range(1, int(no_of_namespaces) + 1):
        get_pods = "cd /home/administrator;kubectl get pod --namespace=namespace-{} | grep postgres | awk '{{print$1}}'".format(ns)
        stdina, stdouta, stderra = client.exec_command(get_pods)
        for pod in stdouta.readlines():
            # print("DATA LOAD FOR THE POD{}".format(pod.rstrip()))
            pod_name = pod.rstrip()

            thislist = ["tpcc_postgres.sql", "Runinside_Postgres.sh"]  #7.5G of data for VMWARE

            for filelist in thislist:
                # print("COPY FILE TO POD'S NATIVE FILESYSTEM")
                kubectl_cp = "kubectl cp /home/administrator/software/Postgresql/{} --namespace=namespace-{} {}:/tmp/".format(filelist,ns,pod_name)
                execommand(kubectl_cp)

            # print("ADD DATA BY ENTERING POSTGRESQL PROMPT")
            load_data = "kubectl -it exec {} --namespace=namespace-{} -- bash -c \"sh /tmp/Runinside_Postgres.sh\"".format(pod_name,ns)
            execommand(load_data)
    # print("#############################################")
    client.close()
fh.close()