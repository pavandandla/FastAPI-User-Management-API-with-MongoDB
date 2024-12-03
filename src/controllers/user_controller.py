# controllers/user_controller.py
from fastapi import APIRouter, Request
from middlewares import token_required, admin_required,user_or_admin_required
from services.user_services import (
    create_user_service,
    get_user_service,
    get_all_users_service,
    delete_user_service,
    update_user_service,
    login_user_service
)


async def create_user(request: Request):
    form_data = await request.json()
    return await create_user_service(form_data)
   

async def login_user(request: Request):
    login_data = await request.json()
    return await login_user_service(login_data)

@token_required
@user_or_admin_required
async def get_user(request: Request,user_id: str):
    return await get_user_service(user_id)

@token_required
@admin_required
async def get_all_users(request: Request):
    return await get_all_users_service()

@token_required
@admin_required
async def delete_user(request: Request,user_id: str):
    return await delete_user_service(user_id)


@token_required
@user_or_admin_required
async def update_user(request: Request, user_id: str, updated_data: dict):
    #updated_data = await request.json()  # Fetch JSON data if `request` is actually a Request
    return await update_user_service(user_id, updated_data)

