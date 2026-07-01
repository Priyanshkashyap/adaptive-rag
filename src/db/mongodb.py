"""
MongoDB configuration.
"""

from pymongo import MongoClient

from src.config.settings import settings


def get_mongo_client() -> MongoClient: # MongoClient is the class provided by PyMongo that knows how to connect to a MongoDB server.
    """
    Create Mongo client.
    """

    return MongoClient(
        settings.mongodb_url
    )


def get_database():
    """
    Return database instance.
    """

    client = get_mongo_client()

    return client[
        settings.mongodb_database #  returns a database object with name 
    ]