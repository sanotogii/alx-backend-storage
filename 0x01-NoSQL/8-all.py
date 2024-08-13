#!/usr/bin/env python3
"""
Lists all documents in a collection.
"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    """
    docs = []
    for doc in mongo_collection.find():
        docs.append(doc)
    return docs
