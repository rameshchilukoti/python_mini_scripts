# READ ME #
# This script will copy a file from a desired host to "N" number of destinations
# Provided the destination hosts are reachable through SSH
# Create a file named destination_servers.txt with list of Client IP's
# For transferring to multiple clients, use the ones with same credentials
import pysftp as sftp

source_host = '10.198.49.200'                # Change into your PPDM/Source IP
source_username = 'admin'                  # Change into your PPDM/Source username
source_password = 'Changeme@1'             # Change into your PPDM/Source Password
destination_username = 'administrator'     # Change into your Kuberenets master username
destination_password = 'emclegato'         # Change into your Kuberenets master password
destination_filepath = "/home/administrator/PPDMCTL"  # Destinaton folder in your Kuberenets master
no_of_namespaces ="3"

def pull_file_from_server():
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=source_host, username=source_username, password=source_password, cnopts=cnopts)
    local_path = "ppdmctl.tar.gz"
    remote_path = "/usr/local/brs/lib/cndm/misc/ppdmctl.tar.gz"
    s.get(remote_path, local_path)
    s.close()

pull_file_from_server()


fh = open('destination_servers.txt')
for f in fh:
    destination_host = f.rstrip()
    print("Copying the file to {}".format(destination_host))

    def push_file_to_server():
        cnopts = sftp.CnOpts()
        cnopts.hostkeys = None
        s = sftp.Connection(host=destination_host, username=destination_username, password=destination_password, cnopts=cnopts)
        local_path = "./ppdmctl.tar.gz"
        remote_path = "{}/ppdmctl.tar.gz".format(destination_filepath)
        s.execute("cd /home/administrator/;rm -rf PPDMCTL; mkdir PPDMCTL".format(destination_filepath))
        s.put(local_path, remote_path)

        s.execute("cd {}/;tar -xvf ppdmctl.tar.gz".format(destination_filepath))

        s.execute(
            "cd /{}/ppdmctl;./ppdmctl applicationtemplate create mysqltemplate --type=mysql --namespace=namespace-3".format(destination_filepath))
        s.execute("cd {}/ppdmctl;./ppdmctl applicationtemplate enable mysqltemplate --namespace=namespace-3".format(destination_filepath))

        #MYSQL
        for i in range(1, int(no_of_namespaces) + 1):
            s.execute("cd /{}/ppdmctl;./ppdmctl applicationtemplate create mysqltemplate --type=mysql --namespace=namespace-{}".format(destination_filepath,i))
            s.execute("cd {}/ppdmctl;./ppdmctl applicationtemplate enable mysqltemplate --namespace=namespace-{}".format(destination_filepath,i))

        #MONGODB
        # s.execute("cd {}/ppdmctl;./ppdmctl template create mongodbtemplate --type=mongodb --namespace=namespace-2".format(destination_filepath))
        # s.execute("cd {}/ppdmctl;./ppdmctl template disable mongodbtemplate --namespace=namespace-2".format(destination_filepath))


     #POSTGRESQL
        s.execute("cd /home/administrator/PPDMCTL/ppdmctl/examples;sed -i '0,/app=postgresql/s/app=postgresql/app=hellokubernetes-postgres/' postgresAppTemplate.json")
        for i in range(3, int(no_of_namespaces) + 1):
            change_namespace ="cd /home/administrator/PPDMCTL/ppdmctl/examples;sed -i '0,/namespace\": \"postgres/s/namespace\": \"postgres/namespace\": \"namespace-{}/' postgresAppTemplate.json".format(i)
            create_ ="cd /home/administrator/PPDMCTL/ppdmctl;./ppdmctl applicationtemplate create postgresAppTemplate --namespace=namespace-{} --inputfile=/home/administrator/PPDMCTL/ppdmctl/examples/postgresAppTemplate.json".format(i)
            change_namespace_back ="cd /home/administrator/PPDMCTL/ppdmctl/examples;sed -i '0,/namespace\": \"namespace-{}/s/namespace\": \"namespace-{}/namespace\": \"postgres/' postgresAppTemplate.json".format(i,i)
            print(change_namespace,create_,change_namespace_back)
            s.execute(change_namespace)
            s.execute(create_)
            s.execute(change_namespace_back)
        s.execute("kubectl get applicationtemplate --all-namespaces")
        s.execute(
            "cd /home/administrator/PPDMCTL/ppdmctl/examples;sed -i '0,/app=postgresql/s/app=postgresql/app=hellokubernetes-postgres/' postgresAppTemplate.json")

       # #CASSANDRA
       #  for i in range(1, int(no_of_namespaces) + 1):
       #      change_namespace = "cd /home/administrator/PPDMCTL/ppdmctl/examples;sed -i '0,/namespace\": \"cassandra/s/namespace\": \"cassandra/namespace\": \"namespace-{}/' cassandraTemplate.json".format(
       #          i)
       #      create_ = "cd /home/administrator/PPDMCTL/ppdmctl;./ppdmctl applicationtemplate create cassandraTemplate --namespace=namespace-{} --inputfile=/home/administrator/PPDMCTL/ppdmctl/examples/cassandraTemplate.json".format(
       #          i)
       #      change_namespace_back = "cd /home/administrator/PPDMCTL/ppdmctl/examples;sed -i '0,/namespace\": \"namespace-{}/s/namespace\": \"namespace-{}/namespace\": \"cassandra/' cassandraTemplate.json".format(
       #          i, i)
       #      print(change_namespace, create_, change_namespace_back)
       #      s.execute(change_namespace)
       #      s.execute(create_)
       #      s.execute(change_namespace_back)
        s.execute("kubectl get applicationtemplate --all-namespaces")
        s.close()

    push_file_to_server()