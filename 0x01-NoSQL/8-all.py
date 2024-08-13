#!/usr/bin/env python3
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    """
    if mongo_collection.find().count() == 0:
        return []
    return list(mongo_collection.find())
