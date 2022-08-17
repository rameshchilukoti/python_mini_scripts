import paramiko
import string
import random
import time
import re
username = "root"
password = "emclegato"
fh = open('hadoopclusterIp.txt')

def randomString(stringLength=10):
   """Generate a random string of fixed length """
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(stringLength))

#Variables
su_hdfs ="runuser -l  hdfs -c 'cd /var/lib/hadoop-hdfs"
list_hdfs = "{};hdfs dfs -ls /".format(su_hdfs)
hdfs_directory = "test{}".format(randomString(3))
hdfs_filename = "testfile{}".format(randomString(5))

config_folder = "/var/lib/hadoop-hdfs/PowerProtect_Hadoop_Data_Protection"


sed_dlp_full_backup = "sed -i '/verify_distcp/s/verify_distcp/#verify_distcp/' dlp-full-backup.sh"


#Executable Commands

Change_sed_dlp_full_backup="{};cd {}/libexec;{}'".format(su_hdfs,config_folder,sed_dlp_full_backup)
list_backup = "{};cd {}/bin;./dlp-backuplist.sh -z ../config/dlpm-env.cfg'".format(su_hdfs,config_folder)

full_backup_command ="{};cd {}/bin;./dlp-admin.sh -b full -z ../config/dlpm-env.cfg'".format(su_hdfs,config_folder)
list_backup = "{};cd {}/bin;./dlp-backuplist.sh -z ../config/dlpm-env.cfg'".format(su_hdfs,config_folder)



for f in fh:
    host = f.rstrip()

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

    execommand(Change_sed_dlp_full_backup)
    execommand(list_backup)
    execommand(full_backup_command)
    execommand(list_backup)

    client.close()
fh.close()