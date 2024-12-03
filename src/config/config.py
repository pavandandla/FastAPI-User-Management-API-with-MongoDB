import os
from dotenv import load_dotenv

load_dotenv()



class Config:
    MONGO_URI = os.getenv("MONGO_URI")  # MongoDB connection URI
    SECRET_KEY = os.getenv("SECRET_KEY")  # JWT secret key
