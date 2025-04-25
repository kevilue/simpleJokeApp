# Tests for the simple joke web app
# using pytest

import pytest

from dotenv import load_dotenv
import os
import pymongo


def test_environment():
    """Test if the environment variables are present."""

    # Try loading a .env file
    try:
        load_dotenv()
    except:
        print("No .env file found.")
    # Get environment variable
    try:
        connectionString = os.environ["MONGO_URI"]
    except:
        connectionString = ""
    # Check if it has content
    assert connectionString != "", "Environment variable MONGO_URI is empty."
    

def test_database_connection():
    """Test if the database connection can be established."""

    # Load environment
    try:
        load_dotenv()
    except:
        print("No .env file found.")
    try:
        connectionString = os.environ["MONGO_URI"]
    except:
        connectionString = ""

    # Try connecting to the database
    mongoclient = pymongo.MongoClient(connectionString)
    assert type(mongoclient) == pymongo.MongoClient, "Failed to connect to the database with connection string: " + str(connectionString)