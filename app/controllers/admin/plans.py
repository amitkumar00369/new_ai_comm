from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi import Depends,Request
from app.middleware.auth_middleware import jwt_auth,jwt_auth_admin
from app.utils.enum import userType
from app.schemas.planSchema import create
from fastapi.concurrency import run_in_threadpool


async def creatPlan(data: create,admin = Depends(jwt_auth_admin)):
    try:
        payload = jsonable_encoder(data)
        await run_in_threadpool()
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        