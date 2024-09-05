from pymongo import MongoClient, errors
import os
import certifi

mongoUrl = os.environ.get('BASE_URL')
try:
    client = MongoClient(mongoUrl, tlsCAFile=certifi.where())
    db = client.page_db
    collection_category = db["Category"]
    collection_product = db["Product"]
    collection_auth = db["Auth"]
    collection_cart = db["Cart"]
    collection_order = db["Order"]
except errors.ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")
except errors.ServerSelectionTimeoutError as e:
    print(f"Server selection timeout: {e}")
except errors.ConfigurationError as e:
    print(f"Configuration error: {e}")
except errors.PyMongoError as e:
    print(f"PyMongo error: {e}")
