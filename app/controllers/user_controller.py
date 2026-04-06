from operator import ge

from fastapi import FastAPI, Response, Request
from pyexpat.errors import messages
from starlette import status

from ..services.passwordService import PasswordService
from app.services.sessionService import SessionService
from ..services.user_service import UserService
from app.utils.enum import userType
from app.schemas.user_schema import signupValidation,loginValidation,changePasswordValidation, changeEmail



from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
from app.utils.constants import generateUserId


# app = FastAPI()
# @app.post("/createData")
async def create_user(data: signupValidation):
    payload = jsonable_encoder(data)

    payload['password'] = PasswordService.createPassword(payload['password'])
    payload['userType'] = userType.user
    payload["userId"] = generateUserId()
    print(payload)
    resData = await run_in_threadpool(UserService.createUser,  payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=resData)

async def userLogin(data: loginValidation):
    payload = jsonable_encoder(data)
    userData = await run_in_threadpool(UserService.getUserByEmail, payload["email"])

    verifyPassword = PasswordService.verifyPassword(payload['password'], userData["password"])
    # print(verifyPassword)

    if not verifyPassword:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN)

    payload = {
        "is_active":True
    }
    tokenPayload = {
        "userId": userData["id"],
    }
    token = await run_in_threadpool(SessionService.createSession, tokenPayload)
    # print(token)
    if not token:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    refreshToken = await run_in_threadpool(SessionService.createRefreshSession, tokenPayload)
    # print(refreshToken)
    sessionData = {
        "userId":userData["id"],
        "email":userData["email"],
        "userType": userType.user,
        "accessToken": token,
        "deviceId": "android",
        "deviceToken": "xva98hjd82gd892v8dnjs8ub37vdu2ug8y93hd8",
        "deviceTypeId": "abc12345"
    }
    # print("dashDB",sessionData)
    session = await run_in_threadpool(SessionService.createSessionData, sessionData)
    payload [ "refreshToken"] = refreshToken

    updateData = await run_in_threadpool(UserService.findByIdUpdate, userData['id'],payload)
    updateData['accessToken'] = token
    updateData['refreshToken'] = refreshToken
    return JSONResponse(status_code=status.HTTP_200_OK, content=updateData)

async def get_user(request: Request):

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok","data": request.state.user,"status":status.HTTP_200_OK})

async def changePassword(request: Request,data: changePasswordValidation):
    try:
        payload = jsonable_encoder(data)
        user = request.state.user
        print("user....................",user)
        verifyPassword = PasswordService.verifyPassword(payload['old_password'], user['password'])
        if not verifyPassword:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "password is wrong"})
        updatePayload = {
            "password": PasswordService.createPassword(payload["new_password"])
        }
        await run_in_threadpool(SessionService.deleteSessionByUserId,user['id'] )
        updateUser = await run_in_threadpool(UserService.findByIdUpdate, user['id'], updatePayload)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok","status":status.HTTP_200_OK})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e)})

async def changeEmailAddress(request: Request, data: changeEmail):
    try:
        payload = jsonable_encoder(data)
        user = request.state.user
        if user['email'] != payload['email']:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "email is wrong"})
        if '@' not in payload['email'] or '.' not in payload['email']:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Invalid email"})
        updatePayload = {
            "email": payload['email'],
        }
        updateUser = await run_in_threadpool(UserService.findByIdUpdate, user['id'], updatePayload)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok", "status": status.HTTP_200_OK})

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e)})



