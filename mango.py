from pymongo import MongoClient

client = MongoClient(host: 'localhost', port: 27017)
db = client['USERS']
persons = db.persons

doc = {
    'name': 'John Doe',
    'age': 30,
    'city': 'New York'
}

persons.insert_one(doc)

for doc in persons.find():
    pprint(doc)