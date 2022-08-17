import pysftp as sftp
import paramiko
import time

username = "administrator"
password = "emclegato"      # Change into your Kuberenets master password
destination_filepath = "/home/administrator/PPDMCTL"  # Destinaton folder in your Kuberenets master
# cidr = "10.125.12.0"
# subnet_mask ="22"

cidr = "10.98.184.0"
subnet_mask ="23"
serviceSubnet ="{}/{}".format(cidr, subnet_mask)

master ="10.98.184.133"
workers = "10.98.184.134", ""
folder = "/home/administrator/automation"
client = paramiko.SSHClient()

def getClient(host):
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    return client

def execommand(client,thecommand):
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

def pull_file_from_server(host,file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder,file)
    print("Downloading file from {} to {}".format(remote_path,local_path))
    s.get(remote_path, local_path)
    s.close()

def edit_local_file(file):
    with open("foo.txt", "r+") as f:
        old = f.read()  # read everything in the file
        f.seek(0)  # rewind
        f.write("new line\n" + old)  # write the new line before

# import sys
# import fileinput
#
# # replace all occurrences of 'sit' with 'SIT' and insert a line after the 5th
# for i, line in enumerate(fileinput.input('lorem_ipsum.txt', inplace=1)):
#     sys.stdout.write(line.replace('sit', 'SIT'))  # replace 'sit' and write
#     if i == 4: sys.stdout.write('\n')  # write a blank line after the 5th line


def push_file_to_server(host, file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder, file)
    print("Uploading file from {} to {}".format(local_path,remote_path))
    s.put(local_path, remote_path)
    s.close()

#Master  - Install Kubernetes
host=master
print("In master ".format(host))
client = getClient(host)
execommand(client,"mkdir {}".format(folder))
set_up_flannel = "echo \"{}\" | sudo -S sysctl net.bridge.bridge-nf-call-iptables=1".format(password)
execommand(client, set_up_flannel)
push_file_to_server(host,"kubeadminit.yaml")
execommand(client,"echo \"{}\" | sudo -S sudo cp {}/kubeadminit.yaml /etc/kubernetes/kubeadminit.yaml".format(password, folder))
install_file_kubeadminit = "echo \"{}\" | sudo -S sudo kubeadm init --config /etc/kubernetes/kubeadminit.yaml".format(password)
output = execommand(client,install_file_kubeadminit)
print(output)
# if(output.__contains__("*kubeadm join*")):
execommand(client, "mkdir -p $HOME/.kube")
execommand(client, "echo \"{}\" | sudo -S sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config".format(password))
execommand(client, "echo \"{}\" | sudo -S sudo chown $(id -u):$(id -g) $HOME/.kube/config".format(password))
time.sleep(150)
execommand(client, "kubectl get pods --namespace=kube-system")
push_file_to_server(host,"kube-flannel-old.yaml")
execommand(client," ")
execommand(client, "kubectl get pods --namespace=kube-system")
execommand(client, "cd {};kubectl -n kube-public get configmap cluster-info -o jsonpath='{{.data.kubeconfig}}' > discovery.yaml".format(folder))
pull_file_from_server(host, "discovery.yaml")
host=workers
# for h in host:
#     print("In Worker {}".format(h))
#     client = getClient(h)
#     execommand(client, "mkdir {}".format(folder))
#     execommand(client, set_up_flannel)
#     push_file_to_server(h, "discovery.yaml")
#     execommand(client,"echo \"{}\" | sudo -S sudo cp {}/discovery.yaml /etc/kubernetes/discovery.yaml".format(password,folder))
#     push_file_to_server(h, "kubeadminitworker.yaml")
#     execommand(client,"echo \"{}\" | sudo -S sudo cp {}/kubeadminitworker.yaml /etc/kubernetes/kubeadminitworker.yaml".format(password,folder))
#     execommand(client, "echo \"{}\" | sudo -S sudo kubeadm join --config /etc/kubernetes/kubeadminitworker.yaml".format(password))
host=master
print("In master ".format(host))
client = getClient(host)
execommand(client,"kubectl get nodes -o wide")
time.sleep(70)
execommand(client, "kubectl get pods --namespace=kube-system")







