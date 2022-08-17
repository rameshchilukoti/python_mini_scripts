import paramiko
import re
import pysftp as sftp

username = "administrator"
password = "emclegato"
folder = "/home/administrator/automation"
fh = open('kworkers.txt')
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

    push_file_to_server(host,"daemon.json")

    # certificate = "openssl s_client -servername ap-sc.lss.emc.com -connect ap-sc.lss.emc.com:8446 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > certificate.crt"
    certificate = "openssl s_client -servername ap-sc.drm.ops.lab.dell.com -connect ap-sc.drm.ops.lab.dell.com:8446 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > certificate.crt"


    chmod = "chmod 644 certificate.crt"

    copy = "echo \"{}\" | sudo -S sudo cp certificate.crt /usr/local/share/ca-certificates/".format(password)

    cd_ls = "cd /usr/local/share/ca-certificates/;ls"

    update = "echo \"{}\" | sudo -S sudo update-ca-certificates".format(password)

    daemon = "cat /home/administrator/automation/daemon.json;echo \"{}\" | sudo -S sudo cp /home/administrator/automation/daemon.json /etc/docker/daemon.json;echo \"{}\" | sudo -S sudo cat /etc/docker/daemon.json".format(password,password)

    restart_docker = "echo \"{}\" | sudo -S sudo systemctl restart docker".format(password)

    execommand(certificate)
    execommand(chmod)
    execommand(copy)
    execommand(cd_ls)
    execommand(update)
    execommand(daemon)
    execommand(restart_docker)
