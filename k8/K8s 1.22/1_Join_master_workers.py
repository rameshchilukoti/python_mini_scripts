import pysftp as sftp
import paramiko
import time

username = "administrator"
password = "emclegato"      # Change into your Kuberenets master password
destination_filepath = "/home/administrator/PPDMCTL"  # Destinaton folder in your Kuberenets master

master ="10.198.184.202"
workers = "10.198.184.203", ""
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


def push_file_to_server(host, file):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    local_path = file
    remote_path = "{}/{}".format(folder, file)
    print("Uploading file from {} to {}".format(local_path,remote_path))
    s.put(local_path, remote_path)
    s.close()

##### Master node
host=master
print("In master {}".format(host))
client = getClient(host)
execommand(client, "mkdir {}".format(folder))
#root user
execommand(client, "echo \"{}\" | sudo -S kubeadm init --apiserver-advertise-address={} --pod-network-cidr=10.244.0.0/16 \n".format(password,master))
time.sleep(10)
execommand(client,"kubectl get pods -A")

# Administrator user
execommand(client, "mkdir -p $HOME/.kube")
execommand(client, "echo \"{}\" | sudo -S sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config".format(password))
execommand(client, "echo \"{}\" | sudo -S sudo chown $(id -u):$(id -g) $HOME/.kube/config".format(password))
time.sleep(10)
get_pods = "kubectl get pods -A"
execommand(client, get_pods)


execommand(client, "kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")
time.sleep(30)
execommand(client, "kubectl get pods -A")

join_command = execommand(client, "echo \"{}\" | sudo -S sudo kubeadm token create --print-join-command".format(password))
print(join_command)
join_command = ''.join(join_command)

#######  Worker nodes
host = workers
for h in host:
    print("In Worker {}".format(h))
    client = getClient(h)
    execommand(client, "mkdir {}".format(folder))
    execommand(client, "echo \"{}\" | sudo -S {}".format(password, join_command))

host = master
print("In master {}".format(host))
time.sleep(30)
client = getClient(host)
execommand(client, "kubectl get nodes -o wide")
execommand(client, "kubectl get pods --namespace=kube-system")







