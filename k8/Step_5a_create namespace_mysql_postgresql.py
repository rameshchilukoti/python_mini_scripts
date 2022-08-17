import paramiko
import time
import re
import pysftp as sftp
username = "administrator"
password = "emclegato"
no_of_namespaces = "10"
no_of_mysqlpods = "0"
no_of_postgresql = "5"
mysql_secret_password = '"emclegato"'
storageClass_name = "sc-common"
print(mysql_secret_password)
folder = "/home/administrator/automation"


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
            # print("{}".format(i))
            output.append(i)
        for i in stderra.readlines():
            print('\x1b[1;31m' + i + '\x1b[0m')
        return output
    def printOutPut(list):
        for i in list:
            print(i)

    # change_storage_class = "cd /home/administrator/automation;grep -rli '\bsc-common\b' * | xargs -i@ sed -i 's/sc-common/{}/g' @".format(storageClass_name)
    # create_storage_class = "cd /home/administrator/automation;kubectl create -f global-storageclass.yml"
    get_storage_class = "kubectl get storageclass {}".format(storageClass_name)
    # execommand(change_storage_class)
    # execommand(create_storage_class)
    execommand(get_storage_class)
    # execommand(change_storage_class)
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

    push_file_to_server(host,"deployment-postgres.yaml")
    for i in range(1, int(no_of_namespaces)+1):
        print("i is {}".format(i))
        change_namespace = "cd /home/administrator/automation; sed -i 's/name: namespace/name: namespace-{}/g' namespace.yaml".format(i)
        createNameSpace = "cd /home/administrator/automation;kubectl apply -f namespace.yaml"
        create_mysql_secret = "cd /home/administrator/automation;kubectl create secret generic mysql --from-literal=password={} --namespace=namespace-{}".format(mysql_secret_password, i)
        create_postgresql_secret = "cd /home/administrator/automation;kubectl apply -f secret-postgres_NoNamespace.yaml --namespace=namespace-{}".format(i)
        change_namespace_back = "cd /home/administrator/automation; sed -i 's/name: namespace-{}/name: namespace/g' namespace.yaml".format(i)
        execommand(change_namespace)
        list = execommand(createNameSpace)
        printOutPut(list)

        list=execommand(create_mysql_secret)
        printOutPut(list)

        list=execommand(create_postgresql_secret)
        printOutPut(list)

        execommand(change_namespace_back)
        for j in range(1, int(no_of_mysqlpods)+1):
            print("#####################################  j is {}".format(j))
            # create sql PV
            change_pv_name = "cd /home/administrator/automation;sed -i 's/name: mysql-persistent-storage/name: mysql-persistent-storage{}/g' MySql-pvc.yaml".format(j)
            create_sql_pv = "cd /home/administrator/automation;kubectl apply -f MySql-pvc.yaml --namespace=namespace-{}".format(i)
            get_pv = "kubectl get pvc --namespace=namespace-{}".format(i)
            # create sql POD
            change_pod_name = "cd /home/administrator/automation;sed -i '0,/name: mysql/s/name: mysql/name: mysql{}/' Mysql_Deployment.yaml".format(j)
            # change_app_name = "cd /home/administrator/automation;awk 'NR==1,/app: mysql/{{sub(/app: mysql/, \"app: mysql{}\")}} 1' Mysql_Deployment.yaml".format(j)
            change_claim_name= "cd /home/administrator/automation;sed -i 's/claimName: mysql-persistent-storage/claimName: mysql-persistent-storage{}/g' Mysql_Deployment.yaml".format(j)
            create_pod_sql = "cd /home/administrator/automation;kubectl apply -f Mysql_Deployment.yaml --namespace=namespace-{}".format(i)
            #Change back parameter from pv and pod deployment files
            change_pv_name_back = "cd /home/administrator/automation;sed -i 's/name: mysql-persistent-storage{}/name: mysql-persistent-storage/g' MySql-pvc.yaml".format(j)
            change_pod_name_back = "cd /home/administrator/automation;sed -i 's/name: mysql{}/name: mysql/g' Mysql_Deployment.yaml".format(j)
            change_claim_name_back= "cd /home/administrator/automation;sed -i 's/claimName: mysql-persistent-storage{}/claimName: mysql-persistent-storage/g' Mysql_Deployment.yaml".format(j)
            # change_app_name = "cd /home/administrator/automation;awk 'NR==1,/app: mysql{}/{{sub(/app: mysql{}/, \"app: mysql\")}} 1' Mysql_Deployment.yaml".format(j,j)

            execommand(change_pv_name)
            list =execommand(create_sql_pv)
            printOutPut(list)
            execommand(get_pv)
            execommand(change_pod_name)
            execommand(change_claim_name)
            list =execommand(create_pod_sql)
            printOutPut(list)

            execommand(change_pv_name_back)
            execommand(change_pod_name_back)
            execommand(change_claim_name_back)
            print("Sleep for 75 seconds")

            time.sleep(5)
        for k in range(1,int(no_of_postgresql)+1):
            print("k is {}".format(k))

            #create postgresql PV
            change_postgresql_pv_name = "cd /home/administrator/automation;sed -i 's/ name: postgresql-persistent-storage/ name: postgresql-persistent-storage{}/g' PostgreSQL-pvc.yaml".format(k)
            create_postgresql_pv = "cd /home/administrator/automation;kubectl apply -f PostgreSQL-pvc.yaml --namespace=namespace-{}".format(i)
            get_pv = "kubectl get pvc --namespace=namespace-{}".format(i)
            #create postgresql POD
            change_pod_name = "cd /home/administrator/automation;sed -i '0,/name: hellokubernetes-postgres/s/name: hellokubernetes-postgres/name: hellokubernetes-postgres{}/' deployment-postgres.yaml".format(k)
            change_claim_name= "cd /home/administrator/automation;sed -i 's/claimName: postgresql-persistent-storage/claimName: postgresql-persistent-storage{}/g' deployment-postgres.yaml".format(k)
            create_pod_postgresql = "cd /home/administrator/automation;kubectl apply -f deployment-postgres.yaml --namespace=namespace-{}".format(i)
            #Chnage back parameter from pv and pod deployment files
            change_postgresql_pv_name_back = "cd /home/administrator/automation;sed -i 's/ name: postgresql-persistent-storage{}/ name: postgresql-persistent-storage/g' PostgreSQL-pvc.yaml".format(k)
            change_pgres_pod_name_back = "cd /home/administrator/automation;sed -i 's/name: hellokubernetes-postgres{}/name: hellokubernetes-postgres/1' deployment-postgres.yaml".format(k)
            change_pgres_claim_name_back= "cd /home/administrator/automation;sed -i 's/claimName: postgresql-persistent-storage{}/claimName: postgresql-persistent-storage/g' deployment-postgres.yaml".format(k)

            execommand(change_postgresql_pv_name)
            list =execommand(create_postgresql_pv)
            printOutPut(list)

            execommand(get_pv)
            execommand(change_pod_name)
            execommand(change_claim_name)
            list = execommand(create_pod_postgresql)
            printOutPut(list)

            execommand(change_postgresql_pv_name_back)
            execommand(change_pgres_pod_name_back)
            execommand(change_pgres_claim_name_back)
            print("Sleep for 75 seconds")

            time.sleep(1)
    client.close()
fh.close()