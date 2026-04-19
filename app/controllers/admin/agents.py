from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi import Depends,Request
from app.middleware.auth_middleware import jwt_auth,jwt_auth_admin
from app.utils.enum import userType
from fastapi.concurrency import run_in_threadpool


# async def createPlan()