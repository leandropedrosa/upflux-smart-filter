from pymongo import MongoClient
import os

ATLAS_CONNECTION_STRING = str(os.getenv('ATLAS_CONNECTION_STRING'))
DB_NAME = str(os.getenv('ATLAS_DB_NAME'))
COLLECTION_NAME = str(os.getenv('ATLAS_COLLECTION_NAME'))

class AtlasClient:

   def __init__ (self):
       self.mongodb_client = MongoClient(ATLAS_CONNECTION_STRING)
       self.database = self.mongodb_client[DB_NAME]
   def ping (self):
       return self.mongodb_client.admin.command('ping')

   def get_collection (self):
       collection = self.database[COLLECTION_NAME]
       return collection

   def find (self, collection_name, filter = {}, limit=0):
       collection = self.database[collection_name]
       items = list(collection.find(filter=filter, limit=limit))
       return items