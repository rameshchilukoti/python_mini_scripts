import paramiko
import re
# go2host="10.110.218.252"
# go2username="root"
# go2password="Changeme@1"
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(go2host, username=go2username, password=go2password)
# storage_show = "cd /;./go2 10.110.218.71"
# stdin, stdout, stderr = client.exec_command(storage_show)
password = "emclegato"
username = "sysadmin"
hosts = "10.125.12.45", "10.118.211.14"
for host in hosts:
    #establish ssh connection with DD
    print(host)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    storage_show = "ddboost storage-unit show"
    stdin, stdout, stderr = client.exec_command(storage_show)
    for i in stdout.readlines():
        storage_unit=i.strip().split()
        # print(storage_unit[0])
        deletestorageunit = "ddboost storage-unit delete {}".format(storage_unit[0])
        stdinb, stdoutb, stderrb = client.exec_command(deletestorageunit)
        for i in stdoutb.readlines():
            print("{}".format(i))
        for i in stderrb.readlines():
            print('\x1b[1;31m' + i + '\x1b[0m')

    filesysclean = "filesys clean start"
    stdine, stdoute, stderre = client.exec_command(filesysclean)
    watch_clean = "filesys clean watch"
    stdind, stdoutd, stderrd = client.exec_command(watch_clean)
    user_show="ddboost user show"
    stdina, stdouta, stderra = client.exec_command(user_show)
    for i in stdouta.readlines():
            if(re.search("sysadmin",i)):
               continue
            else:
                ddboost_user = i.strip().split(" -")
                print(ddboost_user[0])
                def execommand(thecommand):
                    stdina, stdouta, stderra = client.exec_command(thecommand)
                    # print(thecommand)
                    for i in stdouta.readlines():
                        print("{}".format(i))
                    for i in stderra.readlines():
                        print('\x1b[1;31m' + i + '\x1b[0m')
                ddboostuserunassign="ddboost user unassign {}".format(ddboost_user[0])
                userdel="user del {}".format(ddboost_user[0])
                #exceute user unassignment and delete
                execommand(ddboostuserunassign)
                execommand(userdel)
client.close()