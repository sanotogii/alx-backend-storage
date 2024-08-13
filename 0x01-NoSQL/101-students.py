#!/usr/bin/env python3
"""function that returns all students sorted by average score"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """function that returns all students sorted by average score"""
    list_top = [
        {
            "$addFields": {
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        {
            "$sort": { "averageScore": -1 }
        }
    ]
    
    return list(mongo_collection.aggregate(list_top))
