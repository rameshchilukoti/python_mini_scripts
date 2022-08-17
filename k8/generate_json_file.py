import json
import random
import string

rows = 3800 # Number of Objects
number_of_documents = 100 # Number of key-value pairs in each object


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_n_documents(number_of_documents):
    result = {}
    result['name'] = randomString(8)
    result['surname'] = randomString(10)
    result['job'] = randomString(15)
    result['country'] = randomString(16)
    result['state'] = randomString(8)
    result['city'] = randomString(10)
    result['age'] = randomString(15)
    result['salary'] = randomString(16)
    for document in range(1, number_of_documents + 1):
        key = randomString(10)
        value = randomString(15)
        result[key] = value
    return result

with open('16mb.json', 'w') as outfile:
    collection = {}
    for x in range(1, int(rows) + 1):
        collec = create_n_documents(number_of_documents)
        collection[x] = collec
    json.dump(collection, outfile,ensure_ascii=False, indent=4)
