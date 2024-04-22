from pymongo import MongoClient

client = MongoClient("mongodb+srv://hiepph:hiep2003@cluster0.owfcn5g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.page_db 

collection_category = db["Category"]

collection_product = db["Product"]

collection_auth = db["Auth"]