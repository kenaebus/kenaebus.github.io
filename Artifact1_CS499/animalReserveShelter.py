from pymongo import MongoClient
from models import animal_from_doc
import json


class animalReserveShelter:
    def __init__(self):
        HOST = 'localhost'
        PORT = '27017'  # Default MongoDB port
        DB = 'animal_reserve_shelter'
        COL = 'animals'

    # Connect to the database

    # Read JSON data from file
        with open('animals.json', 'r') as f:
            animals_data = json.load(f)

        self.client = MongoClient(f'mongodb://{HOST}:{PORT}/')
        self.db = self.client[DB]
        self.collection = self.db[COL]

        print("Connected to the database successfully!")


        # Insert data into collection
        self.collection.delete_many({})
        self.collection.insert_many(animals_data)
        print("Data loaded into MongoDB.")

    # CRUD

    def create(self, animal_dict):
        self.collection.insert_one(animal_dict)

    def read(self, filter=None):
        filter = filter or {}
        documents = list(self.collection.find(filter))
        return [animal_from_doc(doc).to_dict() for doc in documents]

    def update(self, name, updates):
        pass

    def reserve(self, name):
        result = self.collection.update_one({"name": name}, {"$set": {"reserved": True}})
        return result.modified_count > 0
