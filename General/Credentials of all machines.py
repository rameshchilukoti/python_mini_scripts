import csv
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException

##### List of possible usernames

list_username = ["sysadmin", "admin", "administrator", "root", "oracle",  "administrator@vsphere.local"]

##### List of possible Passwords

list_password = ["abc123","Changeme@1", "Changeme@123", "changeme", "Welcome@123", "emclegato", "Emclegato@123", "Falcons@123", "Password@123", "Password123!", "Kashya123!", "Kashya123", "P@ssw0rd", "P3t3rPan", "Abcd!2345"]

##### IP Range

# IP_range = "10.198.184."
IP_range = "10.118.237."
##### CSV related variables
myData = []
file="credentials.csv"
##### Begin
print("IP,Username,Password")

fh = open('ip.txt')
for f in fh:
# for f in range(71, 72):
#     host = IP_range + f.__str__()
    # print("\033[1m" + host + "\033[0m")
    host = f.rstrip()
    cred_found = "true"
    for username,password in [(username,password) for username in list_username for password in list_password]:
            try:
                # print("{},{}".format(username,password))
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=username, password=password,  timeout=10)
                client.close()
            except:
                print("wrong creds : {},{},{}".format(host, username, password))
                cred_found = "false"
                continue
            else:
                # print("{},{},{}".format(host, username, password))
                list = [host, username, password]
                myData.append(list)
                cred_found = "true"
                break
    if(cred_found=="false"):
        list_na = [host, "NA"]
        myData.append(list_na)

    print("mydata= {}".format(myData))

#### Load nested list into CSV
csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE,lineterminator = "\n")
myFile = open('{}'.format(file), 'w')
print("CREATE {} OR REWRITE {}".format(file, file))
with myFile:
   writer = csv.writer(myFile, dialect='myDialect');
   writer.writerows(myData)