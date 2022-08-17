import paramiko
import re

username = "administrator"
password = "emclegato"

fh = open('kworkers.txt')
print("DELETE MONOGO AND CASSANDRA IMAGES FROM WORKERNODES")

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
    namespace_to_delete =["cassandra","mongo"]
    for ns in namespace_to_delete:
        docker_list = "echo \"{}\" | sudo -S sudo docker image ls |grep {} | awk '{{print$3}}' ".format(password, ns)
        print(docker_list)
        stdina, stdouta, stderra = client.exec_command(docker_list)
        for images in stdouta.readlines():
            print(images.rstrip())
            remove_image = "echo \"{}\" | sudo -S sudo docker image remove {}".format(password, images.rstrip())
            execommand(remove_image)

client.close()
fh.close()