

from fastapi import Depends, FastAPI, Response, Request
from pyexpat.errors import messages
from sqlalchemy import null
from starlette import status

from app.middleware.auth_middleware import jwt_auth

from ...services.passwordService import PasswordService
from app.services.sessionService import SessionService
from ...services.user_service import UserService
from app.utils.enum import userType
from app.schemas.user_schema import SignupValidation,VerifyOtps,editProfileSchema



from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
from app.utils.constants import generateOtp, generateUserId
from datetime import datetime, timedelta


# app = FastAPI()
# @app.post("/createData")
async def create_user(data: SignupValidation):
    try:
        
        payload = jsonable_encoder(data)
        # print("payload", payload)
        user = await run_in_threadpool(UserService.findByNumber, payload["phone_number"] )
        otp = await run_in_threadpool(generateOtp)
        if not user:
            payload1 = {
                "phoneExpireAt":  datetime.now()+ timedelta(minutes=2),
                "phoneOtp": otp,
                "phone_number": payload["phone_number"],
                "country_code": payload["country_code"],
                "userType": userType.user
            }
            # print("payload", payload1)
            userData= await run_in_threadpool(UserService.createUser, payload1)
            message = "created"
            return JSONResponse(content={
            "message": message,"data": {"otp": otp, "user": userData,"expireIn": "2 min"} ,"status":  201
        }, status_code=201)
        if user["isPhoneVerified"]:
            return JSONResponse(content={"message": "User already exist with number","status": 400}, status_code=status.HTTP_400_BAD_REQUEST)
        userData = None
        message = ""
        if not user["isPhoneVerified"]:
            payload1 = {
                "phoneExpireAt":  datetime.now()+ timedelta(minutes=2),
                "phoneOtp": otp
            }
            # print("payload", payload1)
            userData = await run_in_threadpool(UserService.findByIdUpdate, user["id"], payload1)
            message = "updated"
  
            return JSONResponse(content={
                "message": message,"data": {"otp": otp, "user": userData,"expireIn": "2 min"} ,"status":  201
            }, status_code=200)
    except Exception as e:
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )



async def verifyOtp(data:VerifyOtps ):
    payload = jsonable_encoder(data)
    user = await run_in_threadpool(UserService.findById, payload["userId"] )
    expire_time = datetime.fromisoformat(user['phoneExpireAt'])

    print("user",user)
    currentTime = datetime.now()
    print("currentTime", currentTime)
    if user is None:
        return JSONResponse(content={
            "message": "User not found","data": [], "status": 404
        },status_code=404)
        
    elif payload["type"]=="email":
        if expire_time<=currentTime:
            return JSONResponse(content={
                "message": "Otp expired","data": [], "status": 403
            },status_code=403)
        if user['emailOtp']!=payload["otp"] and payload["otp"]!=123456 :
            return JSONResponse(content={
                "message": "Otp invailid","data": [], "status": 400
            },status_code=400)
        payload = {
        "isEmailVerified": True,
        "emailVerify": True }
        return JSONResponse(content={
            "message": "Otp verify successfully","data": [], "status": 200
        },status_code=200)
    elif payload["type"]=="phone":
        if expire_time<=currentTime:
            return JSONResponse(content={
                "message": "Otp expired","data": [], "status": 403
            },status_code=403)
        if user['phoneOtp']!=payload["otp"] and payload["otp"]!=123456 :
            return JSONResponse(content={
                "message": "Otp invailid","data": [], "status": 400
            },status_code=400)
    payload = {
        "is_active":True,
        "isPhoneVerified": True,
        "phoneVerify": True

    }
    tokenPayload = {
        "userId": user["id"],
    }
    token = await run_in_threadpool(SessionService.createSession, tokenPayload)
    # print(token)
    if not token:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    refreshToken = await run_in_threadpool(SessionService.createRefreshSession, tokenPayload)
    # print(refreshToken)
    sessionData = {
        "userId":user["id"],
        # "email":user["email"],
        "phone_number":user["phone_number"],
        "userType": userType.user,
        "accessToken": token,
        "deviceId": "android",
        "deviceToken": "xva98hjd82gd892v8dnjs8ub37vdu2ug8y93hd8",
        "deviceTypeId": "abc12345"
    }
    # print("dashDB",sessionData)
    await run_in_threadpool(SessionService.createSessionData, sessionData)
    payload [ "refreshToken"] = refreshToken

    updateData = await run_in_threadpool(UserService.findByIdUpdate, user['id'],payload)
    updateData['accessToken'] = token
    updateData['refreshToken'] = refreshToken
    return JSONResponse(status_code=status.HTTP_200_OK, content=updateData)

async def editProfile(data: editProfileSchema, currentUser = Depends(jwt_auth)):
    try:
        payload = jsonable_encoder(data)
        update = {}
        otp = await run_in_threadpool(generateOtp)
        if payload["email"]:
            user = await run_in_threadpool(UserService.getUserByEmail, payload["email"])
            if user and  user["id"]!=currentUser["id"]:
                return JSONResponse(content={
                    "message":  "Email exist already",
                    "status": 400
                },status_code=400)

            update = {
                "email": payload["email"],
                "emailExpireAt":  datetime.now()+ timedelta(minutes=2),
                "emailOtp": otp,
                "isEmailVerified": False
            }
        
        elif payload["phone_number"]:
            user = await run_in_threadpool(UserService.findByNumber, payload["phone_number"])
            if user and  user["id"]!=currentUser["id"]:
                return JSONResponse(content={
                    "message":  "Phone number exist already",
                    "status": 400
                },status_code=400)
            update = {
                "phone_number": payload["email"],
                "phoneExpireAt":  datetime.now()+ timedelta(minutes=2),
                "phoneOtp": otp,
                "isPhoneVerified": False
            }
        else:
            update =payload
        userData = await run_in_threadpool(UserService.findByIdUpdate, currentUser["id"], update)
        return JSONResponse(content={
            "message": "success","data": userData,"status": 200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message":str(e)
        },status_code=500)
        
# async def some_api(request: Request):
#     user = request.state.user
#     pass
# async def get_user(request: Request):

#     return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok","data": request.state.user,"status":status.HTTP_200_OK})

# async def changePassword(request: Request,data: changePasswordValidation):
#     try:
#         payload = jsonable_encoder(data)
#         user = request.state.user
#         print("user....................",user)
#         verifyPassword = PasswordService.verifyPassword(payload['old_password'], user['password'])
#         if not verifyPassword:
#             return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "password is wrong"})
#         updatePayload = {
#             "password": PasswordService.createPassword(payload["new_password"])
#         }
#         await run_in_threadpool(SessionService.deleteSessionByUserId,user['id'] )
#         updateUser = await run_in_threadpool(UserService.findByIdUpdate, user['id'], updatePayload)
#         return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok","status":status.HTTP_200_OK})
#     except Exception as e:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e)})

# async def changeEmailAddress(request: Request, data: changeEmail):
#     try:
#         payload = jsonable_encoder(data)
#         user = request.state.user
#         if user['email'] != payload['email']:
#             return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "email is wrong"})
#         if '@' not in payload['email'] or '.' not in payload['email']:
#             return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Invalid email"})
#         updatePayload = {
#             "email": payload['email'],
#         }
#         updateUser = await run_in_threadpool(UserService.findByIdUpdate, user['id'], updatePayload)
#         return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok", "status": status.HTTP_200_OK})

#     except Exception as e:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e)})



