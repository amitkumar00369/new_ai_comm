from fastapi import Depends,Request

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
        return JSONResponse(content={
            "message": "user list",
            "data": users,
            "status": 200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        
async def blockUnblocked(id: int,admin = Depends(jwt_auth_admin) ):
    try:
        
        user = await run_in_threadpool(UserService.findById,id)
        if not user:
            return JSONResponse(content={
                "message": "User not found",
                "status": 404
            },status_code=404)
        message = ""
        if user.isBlocked:
            await run_in_threadpool(UserService.findByIdUpdate,{"isBlocked": False})
            message = "User has been blocked"
        else:
            await run_in_threadpool(UserService.findByIdUpdate,{"isBlocked": True})
            message = "User has been Unblocked"
        return JSONResponse(content={
            "message":message,
            "status": 200
        })
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
async def deleleUser(id: int, admin = Depends(jwt_auth_admin)):
    try:
        user = await run_in_threadpool(UserService.findById,id)
        if not user:
            return JSONResponse(content={
                "message": "User not found",
                "status": 404
            },status_code=404)
        await run_in_threadpool(UserService.findByIdUpdate, id, {"isDeleted": True})
        return JSONResponse(content={
            "message": "user deleted successfully",
            "status": 200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        
            
            
            
            
    