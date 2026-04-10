from fastapi import Depends

from app.middleware.auth_middleware import jwt_auth,jwt_auth_admin
from app.services.passwordService import PasswordService
from app.services.sessionService import SessionService
from app.services.user_service import UserService
from app.schemas.adminSchemas import createAdmin
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.concurrency import run_in_threadpool
from starlette import status

from app.utils.enum import userType


async def getUserList(admin = Depends(jwt_auth_admin)):
    try:
        users = await run_in_threadpool(UserService.getList)
    