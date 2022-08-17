import csv
# https://ap-sc.drm.ops.lab.dell.com/artifactory/snapshots/com/emc/dpsg/ecdm/installer/dellemc-ppdm-sw/19.11.0-1-SNAPSHOT/
import paramiko
from colorama import Fore
import glob
import re
import os
file="list.csv"
#file name of CSV   # Change THIS
# my_list = ["10.198.184.", "10.198.185.","10.198.49.","10.198.48.","10.198.50.","10.198.51.","10.226.152.", "10.226.34."]
# thisdict = {
# "10.198.184.": "DPSWAA-184-",
# "10.198.185.": "DPSWAA-185-",
# "10.198.49.": "DPSWAA-49-",
# "10.198.48.": "DPSWAA-48-",
# "10.198.50.": "DPSWAA-50-",
# "10.198.51.": "DPSWAA-51-",
# "10.226.34.": ""
# }

my_list = ["10.226.34."]
thisdict = {
"10.226.34.": ""
}

def generate_dict():
   myData = [['Computer','IP']]
   for key in thisdict:
       for i in range(10,255):
          list = [thisdict[key]+str(i), key+str(i)]
          myData.append(list)
   return myData

csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE,lineterminator = "\n")
myFile = open('{}'.format(file), 'w')
print("CREATE {} OR REWRITE {}".format(file,file))
with myFile:
   writer = csv.writer(myFile, dialect='myDialect');
   myData = generate_dict()
   writer.writerows(myData)
#########Ignre this#######
# range1 = "10.198.184."
# range1 = "10.198.185."
# range1 = "10.198.49."
# range1 = "10.198.48."
# range1 = "10.198.50."
# range1 = "10.198.51."
# range1 = "10.198.52."
# range1 = "10.198.146."
# range1 = "10.226.78."
# range1 = "10.226.79."
# range1 = "10.226.34."
# range1 = "10.226.152."
# range1 = "10.125.12."
#range1 = "10.226.34."

###########################