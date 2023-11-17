import os
import sys

import pymongo
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

from langregister.base import RegistrationClient

load_dotenv()
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


class MongoAtlas(RegistrationClient):
    uri = "mongodb+srv://rajib76:{MONGO_PASSWORD}@cluster0.cp3rxai.mongodb.net/?retryWrites=true&w=majority".format(
        MONGO_PASSWORD=MONGO_PASSWORD)

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

    def add_assistant(self, assistant_record):
        client, db, collection = self.get_client()
        try:
            result = collection.insert_many(assistant_record)
            return result
        except pymongo.errors.OperationFailure:
            print(
                "An authentication error was received. Are your username and password correct in your connection string?")
            sys.exit(1)

    def get_assistant(self, assistant_record):
        client, db, collection = self.get_client()
        docs = list(collection.find({"assistant_name": assistant_record["assistant_name"]}))
        print("docs", docs)
        assistant_id = ""
        file_id = ""
        if len(docs) > 0:
            for doc in docs:
                assistant_id = doc["assistant_id"]
                file_id = doc["file_id"]
            return True, assistant_id, file_id
        else:
            return False

    def update_assistant(self, assistant_record):
        client, db, collection = self.get_client()
        # doc = collection.find_one_and_update({"assistant_name": assistant_record["assistant_name"]},
        #                                      {"$set": {"assistant_id": assistant_record["assistant_id"]}}, new=True)

        doc = collection.find_one_and_update({"assistant_name": assistant_record["assistant_name"]},
                                             {"$set": {"assistant_id": assistant_record["assistant_id"],
                                                       "file_id": assistant_record["file_id"]}}, new=True)
        if doc is not None:
            print("Here's the updated recipe:")
            print(doc)
        else:
            print("No docs updates")
        print("\n")

    def delete_assistant(self, assistant_record):
        pass


if __name__ == "__main__":
    mc = MongoAtlas()
    # assistant_record = [{"assistant_name":"rajib"}]
    # print(mc.add_assistant(assistant_record))
    assistant_record = {"assistant_name": "rajib", "assistant_id": "12345"}
    # print(mc.update_assistant(assistant_record))
    print(mc.get_assistant(assistant_record))
