from bson.objectid import ObjectId
from pymongo import ASCENDING, errors


class UserModel:

    collection = "users"

    def __init__(self, username, email, role, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    def save(self):
        # Insert the user into the MongoDB collection
        result = db.users.insert_one({
            "username": self.username,
            "email": self.email,
            "role": self.role
        })
        # After inserting, set the id of the instance if not already set
        if not self.id:
            self.id = str(result.inserted_id)  # Store the MongoDB ObjectId as a string

    @staticmethod
    def to_dict(user):
        # If user is a dictionary (e.g., from MongoDB query result), access the '_id' key
        return {
            "id": str(user["_id"]),  # Use the '_id' field from the MongoDB document
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
