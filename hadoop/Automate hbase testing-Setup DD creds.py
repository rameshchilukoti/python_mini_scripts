import paramiko
import string
import random
import time
import re
####################
#Consider Modifying these Variables
####################
username = "root"
password = "emclegato"
dd_ip ="10.125.12.44"
dd_user="sysadmin"
dd_password="emclegato"
dd_su ="ashwithasu"
fh = open('hadoopclusterIp.txt')
############################

def randomString(stringLength=10):
   """Generate a random string of fixed length """
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(stringLength))

#Variables
su_hdfs ="runuser -l  hdfs -c 'cd /var/lib/hadoop-hdfs"
hdfs_directory = "test{}".format(randomString(3))
hdfs_filename = "testfile{}".format(randomString(5))
tar_file ="PowerProtect_Hadoop_Data_Protection.tar.gz"
# tar_file_path ="https://dpadswci.lss.emc.com/job/attic/job/tahoe/job/tahoe19.8.0.x/job/tahoe-19.8.0.x/ws/package/dlp_scripted/target"
tar_file_path ="https://dpadswci.cec.lab.emc.com/job/attic/job/tahoe/job/tahoe-main/job/tahoe/ws/package/dlp_scripted/target"
config_folder = "/var/lib/hadoop-hdfs/PowerProtect_Hadoop_Data_Protection"
source_dir = "HDFSSOURCEDIR=\/data1"
dd_target_dir = "DDTARGETDIR=\/shr-backup\/backup-data1"
dd_host = "DDHOST=10.31.140.154"
dd_storage_unit = "DDSTORAGEUNIT=hadoop_kerberos"
dd_usr="DDUSER=ost"
# sed_source_hdfs = "sed -i '0,/{}/s/{}/HDFSSOURCEDIR=\/{}\/' dlpm-env.cfg".format(source_dir,source_dir,hdfs_directory)

sed_source_hdfs = "sed -i '/data1/s/data1/{}/' dlpm-env.cfg".format(hdfs_directory)
sed_ddtarget_hdfs = "sed -i \"s|DDTARGETDIR.*|DDTARGETDIR=/{}{}|\" dlpm-env.cfg".format(hdfs_directory,dd_su)

sed_dd_host = "sed -i '0,/{}/s/{}/DDHOST={}/' dlpm-env.cfg".format(dd_host,dd_host,dd_ip)
sed_dd_su = "sed -i '0,/{}/s/{}/DDSTORAGEUNIT={}/' dlpm-env.cfg".format(dd_storage_unit,dd_storage_unit,dd_su)
sed_dd_user = "sed -i '0,/{}/s/{}/DDUSER={}/' dlpm-env.cfg".format(dd_usr,dd_usr,dd_user)




#Executable commands

# Step 1 : Configure DD credentials
list_hdfs = "{};hdfs dfs -ls /'".format(su_hdfs)
create_hdfs_dir ="{};hdfs dfs -mkdir /{}'".format(su_hdfs,hdfs_directory)
create_hdfs_files = "{};hdfs dfs -touchz /{}/{}'".format(su_hdfs,hdfs_directory,hdfs_filename)
allowSnapShot= "{};hdfs dfsadmin -allowSnapshot /{}'".format(su_hdfs,hdfs_directory)

wget_tar_file ="rm -rf {};wget --no-check-certificate {}/{} -O {}".format(tar_file,tar_file_path,tar_file,tar_file)
untar ="{};rm -rf PowerProtect_Hadoop_Data_Protection;tar -xvf {}'".format(su_hdfs,tar_file)

change_sed_source_hdfs = "{};cd {}/config;{}'".format(su_hdfs,config_folder,sed_source_hdfs)
change_sed_dd_traget_dir = "{};cd {}/config;{}'".format(su_hdfs,config_folder,sed_ddtarget_hdfs)


change_sed_dd_host = "{};cd {}/config;{}'".format(su_hdfs,config_folder,sed_dd_host)
change_sed_dd_su = "{};cd {}/config;{}'".format(su_hdfs,config_folder,sed_dd_su)
change_sed_dd_user = "{};cd {}/config;{}'".format(su_hdfs,config_folder,sed_dd_user)

execute_dd_configuration = "{};cd {}/bin;./dlp-dd-config.sh -a -z ../config/dlpm-env.cfg'".format(su_hdfs,config_folder)

list_backup = "{};cd {}/bin;./dlp-backuplist.sh'".format(su_hdfs,config_folder)


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(dd_ip, username=dd_user, password=dd_password)
stdina, stdouta, stderra = client.exec_command("ddboost storageunit create {}".format(dd_su,dd_user))
print(stdouta.readlines())
client.close()

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
    # execommand("ls -la;pwd")
    execommand(list_hdfs)
    execommand(create_hdfs_dir)
    execommand(list_hdfs)
    execommand(create_hdfs_files)
    execommand(allowSnapShot)
    print(wget_tar_file)
    execommand(wget_tar_file)
    execommand(untar)
    execommand(change_sed_source_hdfs)
    execommand(change_sed_dd_traget_dir)
    execommand(change_sed_dd_host)
    execommand(change_sed_dd_su)
    execommand(change_sed_dd_user)
    execommand(list_backup)
    print("Run manually -> {}".format(execute_dd_configuration))


    client.close()
fh.close()