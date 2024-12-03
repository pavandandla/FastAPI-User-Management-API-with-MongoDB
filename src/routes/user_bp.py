from fastapi import APIRouter
from controllers.user_controller import (
      create_user,
      login_user,
      get_user,
      get_all_users,
      delete_user,
      update_user
)

# Create a FastAPI APIRouter
user_bp = APIRouter()


user_bp.add_api_route("/create-user/", create_user, methods=["POST"])
user_bp.add_api_route("/login/", login_user, methods=["POST"])
user_bp.add_api_route("/get-user/{user_id}", get_user, methods=["GET"])
user_bp.add_api_route("/get-all-users/", get_all_users, methods=["GET"])
user_bp.add_api_route("/delete-user/{user_id}", delete_user, methods=["DELETE"])
user_bp.add_api_route("/update-user/{user_id}", update_user, methods=["PATCH"])




