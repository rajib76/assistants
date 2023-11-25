import os
import sys

import pymongo
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

from assistants.langregister.base import RegistrationClient

load_dotenv()
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


class MongoAtlas(RegistrationClient):
    uri:str=""

    def get_client(self):
        try:
            client = pymongo.MongoClient(self.uri, server_api=ServerApi('1'))
            db = client.assistantstore
            collection = db["assistants"]
            return client, db, collection
            # return a friendly error if a URI error is thrown
        except pymongo.errors.ConfigurationError:
            print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
            sys.exit(1)
        except Exception as e:
            print(e)

    def add_assistant(self, assistant_record):
        client, db, collection = self.get_client()
        try:
            result = collection.insert_many(assistant_record)
            print("mongo result", result)
            return result
        except pymongo.errors.OperationFailure:
            print(
                "An authentication error was received. Are your username and password correct in your connection string?")
            sys.exit(1)

    def get_assistant(self, assistant_record):
        try:
            client, db, collection = self.get_client()
            docs = list(collection.find({"assistant_name": assistant_record["assistant_name"]}))
            assistant_id = ""
            file_id = ""
            if len(docs) > 0:
                for doc in docs:
                    assistant_id = doc['metadata']["id"]
                    file_id = doc["metadata"]["file_ids"]
                return True, assistant_id, file_id
            else:
                return False
        except Exception as e:
            print(e)

    def update_assistant(self, assistant_record):
        try:
            client, db, collection = self.get_client()
            doc = collection.find_one_and_update({"assistant_name": assistant_record["name"]},
                                                 {"$set": {"metadata": assistant_record}}, new=True)
            if doc is not None:
                print("Assistant information updated in the database")
                print(doc)
            else:
                print("No assistant information updates")
            print("\n")
        except Exception as e:
            print(e)

    def delete_assistant(self, assistant_record):
        pass
