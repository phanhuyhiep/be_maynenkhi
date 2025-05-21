from pymongo import MongoClient, errors
import os
import certifi

mongoUrl = os.environ.get('BASE_URL')
try:
    client = MongoClient(mongoUrl, tlsCAFile=certifi.where())
    db = client.meta_db
    collection_category = db["categories"]
    collection_product = db["products"]
    collection_auth = db["auth"]
    collection_cart = db["carts"]
    collection_order = db["orders"]
except errors.ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")
except errors.ServerSelectionTimeoutError as e:
    print(f"Server selection timeout: {e}")
except errors.ConfigurationError as e:
    print(f"Configuration error: {e}")
except errors.PyMongoError as e:
    print(f"PyMongo error: {e}")
