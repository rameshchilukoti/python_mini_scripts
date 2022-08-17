import pysftp as sftp
import paramiko

destination_username = 'administrator'     # Change into your Kuberenets master username
destination_password = 'emclegato'         # Change into your Kuberenets master password
destination_filepath = "/home/administrator/getDBsize"  # Destinaton folder in your Kuberenets master
no_of_namespaces =1

fh = open('k.txt')
for f in fh:
    destination_host = f.rstrip()
    print("Copying the file to {}".format(destination_host))

    def push_file_to_server():
        cnopts = sftp.CnOpts()
        cnopts.hostkeys = None
        s = sftp.Connection(host=destination_host, username=destination_username, password=destination_password, cnopts=cnopts)
        local_path = "./mysql_get_DB_size.sh"
        s.execute("mkdir {}".format(destination_filepath))
        remote_path = "{}/mysql_get_DB_size.sh".format(destination_filepath)
        s.put(local_path, remote_path)

        local_path = "./Posgres_get_DB_size.sh"
        remote_path = "{}/Posgres_get_DB_size.sh".format(destination_filepath)
        s.put(local_path, remote_path)
        s.close()

    push_file_to_server()
fh.close()
fh = open('k.txt')
for f in fh:
    host = f.rstrip()
    print("\033[1m" + host + "\033[0m")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username="administrator", password="emclegato")


    def execommand(thecommand):
        output = []
        stdina, stdouta, stderra = client.exec_command(thecommand)
        print(thecommand)
        for i in stdouta.readlines():
            print("{}".format(i))
            output.append(i)
        # for i in stderra.readlines():
        #     print('\x1b[1;31m' + i + '\x1b[0m')
        return output
    print("POSGRESQL")
    for naspace in range(1, int(no_of_namespaces) + 1):
        get_pods = "cd /home/administrator;kubectl get pods --namespace=namespace-{} | grep hello | awk '{{print$1}}'".format(
            naspace)
        stdina, stdouta, stderra = client.exec_command(get_pods)
        for pod in stdouta.readlines():
            # print("DATA LOAD FOR THE POD{}".format(pod.rstrip()))
            pod_name = pod.rstrip()

            thislist = ["Posgres_get_DB_size.sh"]

            for filelist in thislist:
                # print("COPY FILE TO POD'S NATIVE FILESYSTEM")
                kubectl_cp = "kubectl cp /home/administrator/getDBsize/{} --namespace=namespace-{} {}:/tmp/".format(
                    filelist, naspace, pod_name)
                execommand(kubectl_cp)

            # print("ADD DATA BY ENTERING POSTGRESQL PROMPT")
            load_data = "kubectl -it exec {} --namespace=namespace-{} -- bash -c \"sh /tmp/Posgres_get_DB_size.sh\"".format(
                pod_name, naspace)
            execommand(load_data)
    print("MYSQL")
    for ns in range(1, int(no_of_namespaces) + 1):
        get_pods = "cd /home/administrator;kubectl get pod --namespace=namespace-{} | grep mysql | awk '{{print$1}}'".format(ns)
        stdina, stdouta, stderra = client.exec_command(get_pods)
        for pod in stdouta.readlines():
            # print("DATA LOAD FOR THE POD{}".format(pod.rstrip()))
            pod_name = pod.rstrip()

            thislist = ["mysql_get_DB_size.sh"]

            for filelist in thislist:
                # print("COPY FILE TO POD'S NATIVE FILESYSTEM")
                kubectl_cp = "kubectl cp /home/administrator/getDBsize/{} --namespace=namespace-{} {}:/tmp/".format(filelist,ns,pod_name)
                execommand(kubectl_cp)

            # print("ADD DATA BY ENTERING POSTGRESQL PROMPT")
            load_data = "kubectl -it exec {} --namespace=namespace-{} -- bash -c \"sh /tmp/mysql_get_DB_size.sh\"".format(pod_name,ns)
            execommand(load_data)


    client.close()
fh.close()