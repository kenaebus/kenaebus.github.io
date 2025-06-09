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
        self.client = MongoClient(f'mongodb://{HOST}:{PORT}/')
        self.db = self.client[DB]
        self.collection = self.db[COL]

    # Read JSON data from file
    def load_data_from_json(self, file_path='animals.json'):
        try:
            with open(file_path, 'r') as f:
                animals_data = json.load(f)
            self.collection.delete_many({})
            self.collection.insert_many(animals_data)
            print("Data loaded into MongoDB.")
        except Exception as e:
            print(f"Error loading data: {e}")
    # CRUD

    def create(self, animal_dict):
        required_fields = ['name',]
        if not required_fields.issubset(animal_dict.keys()):
            raise ValueError("Missing required fields.")
        self.collection.insert_one(animal_dict)

    def read(self, filter=None):
          if not filter:
            return self.animals
        result = self.animals
        for key, value in filter.items():
            result = [a for a in result if str(a.get(key)).lower() == str(value).lower()]
        return result

    def update(self, name, updates):
        result = self.collection.update_one({"name": name}, {"$set": updates})
        return result.modified_count > 0
    

    def reserve(self, name):
        result = self.collection.update_one({"name": name}, {"$set": {"reserved": True}})
        return result.modified_count > 0


    def delete(self, name):
        result = self.collection.delete_one({"name": name})
        return result.deleted_count > 0