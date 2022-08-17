import paramiko
import time
import pysftp as sftp
import re
username = "administrator"
password = "emclegato"
no_of_namespaces = "11"
no_of_mongoDBpods = "1"
no_of_cassandra = "1"
mysql_secret_password = '"emclegato"'
storageClass_name = "sc-common"
print(mysql_secret_password)
folder = "/home/automation/dataload"


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


    def push_file_to_server(host, file):
        cnopts = sftp.CnOpts()
        cnopts.hostkeys = None
        s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
        local_path = file
        remote_path = "{}/{}".format(folder, file)
        print("Uploading file from {} to {}".format(local_path, remote_path))
        s.put(local_path, remote_path)
        s.close()
        # install certificates


    # push_file_to_server(host, "cass_1gb.csv")
    get_storage_class = "kubectl get storageclass {}".format(storageClass_name)
    execommand(get_storage_class)
    for i in range(11 , int(no_of_namespaces)+1):
        print("creating namespace-{}".format(i))
        change_namespace = "cd /home/administrator/automation; sed -i 's/name: namespace/name: namespace-{}/g' namespace.yaml".format(i)
        createNameSpace = "cd /home/administrator/automation;kubectl apply -f namespace.yaml"
        change_namespace_back = "cd /home/administrator/automation; sed -i 's/name: namespace-{}/name: namespace/g' namespace.yaml".format(i)

        execommand(change_namespace)
        execommand(createNameSpace)
        execommand(change_namespace_back)

        for j in range(1, int(no_of_mongoDBpods)+1):
            print("MONGO DB {}".format(j))
            print("CREATE KEY")
            createKey = "openssl rand -base64 741 > key.txt"
            createSecretKey = "kubectl create secret generic shared-bootstrap-data --from-file=internal-auth-mongodb-keyfile=key.txt --namespace=namespace-{}".format(i)
            print("CREATE MONGODB SERVICE")
            create_service = "cd /home/administrator/automation;kubectl apply -f mongodb-service.yaml --namespace=namespace-{}".format(i)
            print("CHNAGE POD, mount name AND PVC NAME")
            change_pod_name = "cd /home/administrator/automation;sed -i '0,/name: mongod/s/name: mongod/name: mongod{}/' mongodb-statefulset.yaml".format(j)
            change_pvc_name = "cd /home/administrator/automation;sed -i 's/name: mongodb-persistent-storage-claim/name: mongodb-persistent-storage-claim{}/g' mongodb-statefulset.yaml".format(j)

            print("CREATE MONGODB STATEFUL SET")
            create_mongodb_stateful_set = "cd /home/administrator/automation;kubectl apply -f mongodb-statefulset.yaml --namespace=namespace-{}".format(i)
            print("CHANGE PVC, mount name and POD NAME BACK TO ORIGINAL")
            change_pvc_name_back = "cd /home/administrator/automation;sed -i 's/name: mongodb-persistent-storage-claim{}/name: mongodb-persistent-storage-claim/g' mongodb-statefulset.yaml".format(j,j)
            change_pod_name_back = "cd /home/administrator/automation;sed -i '0,/name: mongod{}/s/name: mongod{}/name: mongod/' mongodb-statefulset.yaml".format(j,j)

            execommand(createKey)
            execommand(createSecretKey)
            execommand(create_service)
            execommand(change_pod_name)
            execommand(change_pvc_name)
            execommand(create_mongodb_stateful_set)
            execommand(change_pvc_name_back)
            execommand(change_pod_name_back)
            print("Sleep for 150 seconds")

            time.sleep(10)
        for k in range(1, int(no_of_cassandra)+1):
            # cassandra DB
            print("CASSANDRA {}".format(k))
            print("CREATE CASSANDRA SERVICE")
            create_cassandra_service = "cd /home/administrator/automation;kubectl apply -f cassandra-service.yaml --namespace=namespace-{}".format(i)

            print("CHANGE PVC and POD NAMES")
            change_cassandra_pod_name = "cd /home/administrator/automation;sed -i '0,/name: cassandra/s/name: cassandra/name: cassandra{}/' cassandra-statefulset.yaml".format(k)
            change_cassandra_pvc_name = "cd /home/administrator/automation;sed -i 's/name: cassandra-data/name: cassandra-data{}/g' cassandra-statefulset.yaml".format(k)
            change_cassandra_namespace_name = "cd /home/administrator/automation;sed -i 's/cassandra-0.cassandra.default.svc.cluster.local/cassandra{}-0.cassandra.namespace-{}.svc.cluster.local/g' cassandra-statefulset.yaml".format(k,i)
            time.sleep(10)
            print("CRAETE STATEFUL SET")
            create_cassandra_stateful_set = "cd /home/administrator/automation;kubectl apply -f cassandra-statefulset.yaml --namespace=namespace-{}".format(i)
            print("CHANGE PVC, mount name and POD NAME BACK TO ORIGINAL")
            change_cassandra_pvc_name_back = "cd /home/administrator/automation;sed -i 's/name: cassandra-data{}/name: cassandra-data/g' cassandra-statefulset.yaml".format(k, k)
            change_cassandra_pod_name_back = "cd /home/administrator/automation;sed -i '0,/name: cassandra{}/s/name: cassandra{}/name: cassandra/' cassandra-statefulset.yaml".format(k, k)
            change_cassandra_namespace_name_back = "cd /home/administrator/automation;sed -i 's/cassandra{}-0.cassandra.namespace-{}.svc.cluster.local/cassandra-0.cassandra.default.svc.cluster.local/g' cassandra-statefulset.yaml".format(k,i)

            execommand(create_cassandra_service)
            execommand(change_cassandra_pod_name)
            execommand(change_cassandra_pvc_name)
            execommand(change_cassandra_namespace_name)
            execommand(create_cassandra_stateful_set)
            execommand(change_cassandra_pvc_name_back)
            execommand(change_cassandra_pod_name_back)
            execommand(change_cassandra_namespace_name_back)

            print("Sleep for 150 seconds")
            time.sleep(10)
        get_all = "kubectl get all --namespace=namespace-{}".format(i)
        execommand(get_all)
        # time.sleep(600)
    client.close()
fh.close()