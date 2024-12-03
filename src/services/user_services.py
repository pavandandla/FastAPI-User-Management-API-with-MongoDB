from config.database import db
from models.all_models import UserModel
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError  # Import DuplicateKeyError here
import bcrypt
import jwt
import os
from dotenv import load_dotenv


async def create_user_service(form_data):

    # Hash the password
    hashed_password = bcrypt.hashpw(form_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = {
        "username": form_data["username"],
        "email": form_data["email"],
        "password": hashed_password,
        "role": form_data.get("role", "user")
    }
    try:
        # Attempt to insert the new user
        result = await db[UserModel.collection].insert_one(new_user)
        # Fetch the inserted document
        inserted_user = await db[UserModel.collection].find_one({"_id": result.inserted_id})
        return {"status": "success", "statusCode": 201, "message": "User created", "data": UserModel.to_dict(inserted_user)}
    except DuplicateKeyError as e:
        # Check if the error is due to username or email duplication
        error_message = "Username or email already exists."
        if "username" in str(e):
            error_message = "Username already exists."
        elif "email" in str(e):
            error_message = "Email already exists."
        return {"status": "success", "statusCode": 200, "message": error_message}

async def login_user_service(login_data):
    user = await db[UserModel.collection].find_one({"email": login_data["email"]})
    if user and bcrypt.checkpw(login_data["password"].encode('utf-8'), user["password"].encode('utf-8')):
        token_Data = {
                    'role': user["role"],
                    'username': user["username"],
                    'id': str(user["_id"])
                }
                #print("id===>",user.id)
                
                # Encode the token using JWT
        token = jwt.encode(token_Data, str(os.getenv('SECRET_KEY')) , algorithm='HS256')

        return  {
                    'message': f"Login Successful. Welcome, {user['username']}!",
                    'status': "success",
                    'statusCode': 200,
                    'token': token
                }, 200
    
    return {"status": "failed","statusCode": 200,"message": "Invalid email or password"}

async def get_user_service(user_id):
    user = await db[UserModel.collection].find_one({"_id": ObjectId(user_id)})
    if user:
        return {"status": "success","statusCode": 200, "data": UserModel.to_dict(user)}
    return {"status": "failed","statusCode": 200,"message": "User not found"}

async def get_all_users_service():
    users = await db[UserModel.collection].find().to_list(None)
    return {"status": "success","statusCode": 200, "data": [UserModel.to_dict(user) for user in users]}

async def delete_user_service(user_id):
    result = await db[UserModel.collection].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"status": "success","statusCode": 200,"message": "User deleted successfully"}
    return {"status": "failed","statusCode": 200,"message": "User not found"}

async def update_user_service(user_id, updated_data):
    # Check if the updated data contains a password, and if so, hash it
    if "password" in updated_data:
        updated_data["password"] = bcrypt.hashpw(updated_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Check for duplicate username and email if they are in the update data
    if "username" in updated_data:
        existing_user = await db[UserModel.collection].find_one({"username": updated_data["username"]})
        if existing_user: # and str(existing_user["_id"]) != user_id:
            return {"status": "success", "statusCode": 200, "message": "Username already exists."}

    if "email" in updated_data:
        existing_user = await db[UserModel.collection].find_one({"email": updated_data["email"]})
        if existing_user: # and str(existing_user["_id"]) != user_id:
            return {"status": "sucsess", "statusCode": 200, "message": "Email already exists."}

    result = await db[UserModel.collection].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updated_data}
    )
    if result.matched_count == 0:
        return {"status": "failed","statusCode": 200,"message": "User not found"}
    user = await db[UserModel.collection].find_one({"_id": ObjectId(user_id)})
    return {"status": "success","statusCode": 200,"message": "User updated successfully", "data": UserModel.to_dict(user)}
