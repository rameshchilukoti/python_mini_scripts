import paramiko
import time
import re
no_of_namespaces = "1"
username = "administrator"
password = "emclegato"
directory = "automation/dataload"   #directory where
filename = "cass_gen.sh"   #filename which contains the command to create keyspae, table and insert data
keyspace_name = "gen_key"
table_name = "gen_table"
gen_file_name = "cass_1gb.csv"
number_tables = "5"
#do not modify
create_table = "id int,name text,surname text,job text,country text,state text,city text,age int,salary int,PRIMARY KEY(id))"

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
    print("Cassandra dataloading")
    for ns in range(1, int(no_of_namespaces)+1):
        for table in range(1, int(number_tables)+ 1):

            # create_directory = "mkdir /home/administrator/{}".format(directory)
            # pull_gen_file = "cd /home/administrator/{};wget https://raw.githubusercontent.com/AshwithaCrasta/test/master/{}".format(directory,gen_file_name)
            create_file_add_create_keyspace_command = "cd /home/administrator/{};echo -e \"CREATE KEYSPACE {} WITH replication = {{'class':'SimpleStrategy', 'replication_factor' : 2}};\" > {}".format(directory,keyspace_name,filename)
            add_use_key_command = "cd /home/administrator/{};echo -e 'use {};' >> {}".format(directory,keyspace_name,filename)
            add_create_table_command = "cd /home/administrator/{};echo -e 'CREATE TABLE {}{}({};' >> {}".format(directory,table_name,table,create_table,filename)
            add_copy_csv_command ="cd /home/administrator/{};echo -e \"COPY {}{}(id,name,surname,job,country,state,city,age,salary) FROM '/tmp/{}' WITH DELIMITER=',' AND HEADER=TRUE;\" >> {}".format(directory,table_name,table,gen_file_name,filename)
            # add_select_all_command = "cd /home/administrator/{};echo -e 'select * from {};\\nexit\\n' >> {}".format(directory,table_name,filename)
            cat_file = "cd /home/administrator/{}; cat {}".format(directory,filename)
            # execommand(create_directory)
            # execommand(pull_gen_file)
            execommand(create_file_add_create_keyspace_command)
            execommand(add_use_key_command)
            execommand(add_create_table_command)
            execommand(add_copy_csv_command)
            # execommand(add_select_all_command)
            execommand(cat_file)


            get_pods = "cd /home/administrator;kubectl get pod --namespace=namespace-{} | grep cassandra | awk '{{print$1}}'".format(ns)
            list = execommand(get_pods)
            print(list[0].rstrip())

            kubectl_cp = "kubectl cp /home/administrator/{}/{} --namespace=namespace-{} {}:/tmp/".format(directory,filename,ns ,list[0].rstrip())
            execommand(kubectl_cp)
            kubectl_cp_gen_csv = "kubectl cp /home/administrator/{}/{} --namespace=namespace-{} {}:/tmp/".format(directory, gen_file_name, ns,
                                                                                                         list[0].rstrip())
            execommand(kubectl_cp_gen_csv)

            kubectl_add_data_to_table = "kubectl -it exec {} --namespace=namespace-{} -- bash -c \"cqlsh < /tmp/{}\"".format(list[0].rstrip(),ns,filename)
            execommand(kubectl_add_data_to_table)
            time.sleep(75)

client.close()
fh.close()
