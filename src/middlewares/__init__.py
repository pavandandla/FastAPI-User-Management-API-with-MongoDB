# middlewares/__init__.py
from functools import wraps
import jwt
import os
import logging
from fastapi import Request, Response
from models.all_models import UserModel
from config.database import db
from dotenv import load_dotenv
from jwt import ExpiredSignatureError, InvalidTokenError

# Load environment variables
load_dotenv()

def decode_jwt(token):
    try:
        token = token.split(" ")[1]  # Split the token in 'Bearer <token>' format
        return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
    except ExpiredSignatureError:
        logging.error("Token has expired")
        return {'error': 'Token has expired'}
    except InvalidTokenError:
        logging.error("Invalid token")
        return {'error': 'Invalid token'}

def token_required(f):
    @wraps(f)
    async def decorated(request: Request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logging.warning("Missing Authorization header")
            return Response(
                content='{"message": "Unauthorized - Missing Authorization header"}',
                status_code=401,
                media_type="application/json"
            )
        try:
            data = decode_jwt(token)
            if 'error' in data:
                return Response(
                    content=f'{{"message": "Unauthorized - {data["error"]}"}}',
                    status_code=401,
                    media_type="application/json"
                )
            cur_user = await db[UserModel.collection].find_one({"username": data['username']})
            if not cur_user:
                return Response(
                    content='{"message": "User not found"}',
                    status_code=200,
                    media_type="application/json"
                )
        except Exception as e:
            logging.error(f"Token validation failed: {e}")
            return Response(
                content='{"message": "Token is invalid!"}',
                status_code=403,
                media_type="application/json"
            )

        # Inject `cur_user` into the function call
        return await f(cur_user, *args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    async def decorated(cur_user, *args, **kwargs):
        if cur_user.get('role') != 'admin':
            logging.warning("User is not authorized")
            return Response(
                content='{"message": "Unauthorized - Admin access required"}',
                status_code=403,
                media_type="application/json"
            )
        return await f(cur_user, *args, **kwargs)
    return decorated

def user_or_admin_required(f):
    @wraps(f)
    async def decorated(cur_user, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if not user_id:
            return Response(
                content='{"message": "User ID is required"}',
                status_code=400,
                media_type="application/json"
            )
        
        # Admin can update any user, non-admin can only update their own profile
        if cur_user.get('role') != 'admin' and str(cur_user['_id']) != user_id:
            logging.warning("User is not authorized to update this profile")
            return Response(
                content='{"message": "Unauthorized - User can only update their own profile"}',
                status_code=403,
                media_type="application/json"
            )
        return await f(cur_user, *args, **kwargs)
    return decorated











