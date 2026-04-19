

from fastapi import Depends, FastAPI, Response, Request
from pyexpat.errors import messages
from sqlalchemy import null
from starlette import status

from app.middleware.auth_middleware import jwt_auth

from ...services.passwordService import PasswordService
from app.services.sessionService import SessionService
from ...services.user_service import UserService
from ...services.tenant_service import TenatService
from app.utils.enum import userType
from app.schemas.tenant_schema import create

from app.utils.response_data import success_response,error_response
from app.utils.message import HttpStatusCode,SuccessMessage, ErrorMessage


from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
from app.utils.constants import generateTenantId
from datetime import datetime, timedelta


async def createTenat(data: create, user = Depends(jwt_auth) ):
    try:
        Activetenat = await run_in_threadpool(TenatService.findByUserid,user.get("id"))
        if Activetenat is not None:
            return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "You have already active service"}
        )
             
        payload = jsonable_encoder(data)
        payload["user_id"] = user.get("id")
        payload["tenantId"] = await run_in_threadpool(generateTenantId)
        data = await run_in_threadpool(TenatService.createtenant,payload)
        return await run_in_threadpool(success_response, SuccessMessage.CREATED,data,HttpStatusCode.OK)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
async def getTenatDetails(user= Depends(jwt_auth)):
    try:
        Activetenat = await run_in_threadpool(TenatService.findByUserid,user.get("id"))
        if Activetenat is None:
            return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "You have not active service, please create"}
        )
        print(Activetenat)
        return await run_in_threadpool(success_response, SuccessMessage.FETCHED,Activetenat,HttpStatusCode.OK)
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
        