import paramiko
import re
username = "administrator"
password = "emclegato"
no_of_namespaces = "1"
no_of_mongopods = "3"
directory = "mongodb_dataload" #create a new directory
mongo_db_admin = "theadmin"    #db admin username
mongo_db_password = "emclegato"  #db admin password

# Set Main replication Set using rs.inititae
# create Db admin
# Set mongo node priority
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

    mkdir = "cd /home/administrator;mkdir {}".format(directory)
    execommand(mkdir)
    for ns in range(1, int(no_of_namespaces)+1):
        get_pods = "cd /home/administrator/{};kubectl get pod --namespace=namespace-{} | grep mongo | awk '{{print$1}}'".format(directory,ns)
        stdina, stdouta, stderra = client.exec_command(get_pods)


        #create file with "Set Main replication set" commands

        rsinitiateString = "rs.initiate({_id: \"MainRepSet\", version: 1,members: ["
        print("..........namespace-{}".format(ns))
        i = 0
        for pod in stdouta.readlines():
            if i==0 :
                rsinitiateString = "{}{{_id: {}, host: \"{}.mongodb-service.namespace-{}.svc.cluster.local:27017\"}}".format(rsinitiateString,i,pod.rstrip(),ns)
                i=i+1
            elif i== int(no_of_mongopods):
                rsinitiateString = "{}{{_id: {}, host: \"{}.mongodb-service.namespace-{}.svc.cluster.local:27017\"}}".format(rsinitiateString,i,pod.rstrip(),ns)

            else:
                rsinitiateString = "{}{{_id: {}, host: \"{}.mongodb-service.namespace-{}.svc.cluster.local:27017\"}}]}});\\n".format(rsinitiateString,i,pod.rstrip(),ns)
                i=i+1

        print(rsinitiateString)
        create_sh = "cd /home/administrator/{};echo -e '{}' > namespace-{}mongo_initiate.sh".format(directory,rsinitiateString,ns)
        execommand(create_sh)
        cat_script = "cd /home/administrator/{};cat namespace-{}mongo_initiate.sh".format(directory,ns)
        print(cat_script)

        #create file with "Create db user" commands
        list_of_commands = ["use admin", "rs,slaveOk()", "db.createUser( {{ user: \"{}\", pwd: \"{}\", "
                                                         "roles: [ \"userAdminAnyDatabase\", \"readWriteAnyDatabase\", \"dbAdminAnyDatabase\", \"clusterAdmin\" ] }} )".format(mongo_db_admin,mongo_db_password)]
        for command in list_of_commands:
            create_script = "cd /home/administrator/{};echo -e '{}' >> namespace-{}create_DBuser.sh".format(directory,command,ns)
            execommand(create_script)
        cat_script = "cd /home/administrator/{};cat namespace-{}create_DBuser.sh".format(directory,ns)
        execommand(cat_script)

        #create file with "Set priority" commands

        list_of_commands = ["use admin", "rs,slaveOk()","db.auth(\"{}\",\"{}\")",
                            "cfg = rs.conf()","cfg.members[0].priority = 2","cfg.members[1].priority = 0","cfg.members[2].priority = 0".format(mongo_db_admin,mongo_db_password)]
        for command in list_of_commands:
            create_script = "cd /home/administrator/{};echo -e '{}' >> namespace-{}set_priority.sh".format(directory,
                                                                                                 command, ns)
            execommand(create_script)

        cat_script = "cd /home/administrator/{};cat namespace-{}set_priority.sh".format(directory, ns)
        execommand(cat_script)


        pod_list = stdouta.readlines()
        pod_0 = pod_list[0].rstrip()
    # Execute file with "Set Main replication set" commands in POD-0
        kubectl_cp = "kubectl cp /home/administrator/{}/namespace-{}mongo_initiate.sh --namespace=namespace-{} {}:/tmp/".format(directory,ns,ns,pod_0)
        kubectl_exec = "kubectl exec -it {} --namespace=namespace-{} -- bash -c \"mongo < /tmp/namespace-{}mongo_initiate.sh\"".format(pod_0,ns,ns)
        execommand(kubectl_cp)
        execommand(kubectl_exec)
    # Execute file with "Create db user" commands in POD-0
        kubectl_cp = "kubectl cp /home/administrator/{}/create_DBuser.sh --namespace=namespace-{} {}:/tmp/".format(
            directory, ns, ns, pod_0)
        kubectl_exec = "kubectl exec -it {} --namespace=namespace-{} -- bash -c \"mongo < /tmp/namespace-{}create_DBuser.sh\"".format(
            pod_0, ns, ns)
        execommand(kubectl_cp)
        execommand(kubectl_exec)
    #Execute file with "Set priority" commands in POD-0
        kubectl_cp = "kubectl cp /home/administrator/{}/namespace-{}set_priority.sh --namespace=namespace-{} {}:/tmp/".format(
            directory, ns, ns, pod_0)
        kubectl_exec = "kubectl exec -it {} --namespace=namespace-{} -- bash -c \"mongo < /tmp/namespace-{}set_priority.sh\"".format(
            pod_0, ns, ns)
        execommand(kubectl_cp)
        execommand(kubectl_exec)
    client.close()
fh.close()