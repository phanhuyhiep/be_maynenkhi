from pymongo import MongoClient,errors
import os
mongoUrl  = os.environ.get('BASE_URL')
try:
    client = MongoClient(mongoUrl)
    db = client.page_db
    collection_category = db["Category"]
    collection_product = db["Product"]
    collection_auth = db["Auth"]
    collection_cart = db["Cart"]
except errors.ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")