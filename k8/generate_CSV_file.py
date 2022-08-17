import csv
import random
import string
from random import randint
file="cass_1gb.csv"       #file name of CSV   # Change THIS

rows = 15000  # Number rows to   # Change THIS

def randomString(stringLength=10):
   """Generate a random string of fixed length """
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(stringLength))


def random_with_N_digits(n):
   range_start = 10 ** (n - 1)
   range_end = (10 ** n) - 1
   return randint(range_start, range_end)


def generate_dict():
   # myDatainCSv = [[1, 2, 3], ['Good Morning', 'Good Evening', 'Good Afternoon']]
   myData = [['id','name','surname','job','country','state','city','age','salary']]
   for i in range(1,rows +1):
      list = [i,randomString(8),randomString(10),randomString(8),randomString(8),randomString(9),randomString(10),random_with_N_digits(2),random_with_N_digits(6)]
      myData.append(list)
   return myData

csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE,lineterminator = "\n")
myFile = open('{}'.format(file), 'w')
print("CREATE {} OR REWRITE {}".format(file,file))
with myFile:
   writer = csv.writer(myFile, dialect='myDialect');
   myData = generate_dict()
   writer.writerows(myData)