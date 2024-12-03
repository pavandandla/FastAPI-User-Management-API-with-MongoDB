from motor.motor_asyncio import AsyncIOMotorClient
from config.config import Config  # Ensure this imports your MongoDB URI
from models.all_models import UserModel  # Import your UserModel
from pymongo import errors, ASCENDING

# Create a MongoDB client
client = AsyncIOMotorClient(Config.MONGO_URI)
db = client["firstdb"]  # Use the specific database name 'firstdb'

# Ensure unique indexes on 'username' and 'email'
try:
    db[UserModel.collection].create_index([("username", ASCENDING)], unique=True)
    db[UserModel.collection].create_index([("email", ASCENDING)], unique=True)
    print("Unique indexes created on 'username' and 'email'")
except errors.OperationFailure as e:
    print("Index already exists:", e)
