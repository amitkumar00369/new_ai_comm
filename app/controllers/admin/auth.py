from app.services.passwordService import PasswordService
from app.services.sessionService import SessionService
from app.services.user_service import UserService
from app.schemas.adminSchemas import createAdmin
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi.concurrency import run_in_threadpool
from fastapi import Depends,Request
from app.middleware.auth_middleware import jwt_auth,jwt_auth_admin
from app.utils.enum import userType

async def create(data: createAdmin):
    try:
        payload = jsonable_encoder(data)
        payload["password"] = await run_in_threadpool(PasswordService.createPassword,payload['password'])
        payload['userType'] = userType.admin
        resData = await run_in_threadpool(UserService.createUser,  payload)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=resData)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))
    
async def login(data: createAdmin):
    try:
        payload = jsonable_encoder(data)
        print("parrr",payload)

        #  Find user
        admin = await run_in_threadpool(
            UserService.getUserByEmail,
            payload['email']
        )

        if admin is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Admin not found with this email"}
            )

        # 🔐 Verify password
        passwordValid = await run_in_threadpool(
            PasswordService.verifyPassword,
            payload['password'],
            admin["password"]
        )

        if not passwordValid:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Wrong credentials"}
            )

        #  Create token
        tokenPayload = {
            "userId": admin["id"],
        }

        token = await run_in_threadpool(
            SessionService.createSession,
            tokenPayload
        )

        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Token generation failed"}
            )

        #  Save session
        sessionData = {
            "userId": admin["id"],
            "email": admin["email"],
            "userType": userType.admin,
            "accessToken": token,
            "deviceId": "android",
            "deviceToken": "xva98hjd82gd892v8dnjs8ub37vdu2ug8y93hd8",
            "deviceTypeId": "abc12345"
        }

        await run_in_threadpool(
            SessionService.createSessionData,
            sessionData
        )

        # Success response
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "login successfull", "token": token, "status": 200}
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
async def editProfile(data: dict, admin = Depends(jwt_auth_admin)):
    
    try:
        payload = jsonable_encoder(data)
        updateData = {
            "firstName": payload["firstName"],
            "lastName": payload["lastName"],
            "image": payload["image"]
        }
        adminData = await run_in_threadpool(UserService.findByIdUpdate, admin.get("id"), updateData)
        return JSONResponse(content={
            "message": "Profile updated successfully",
            "data": adminData,
            "status": 200
        })
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
async def logout(request: Request,admin=Depends(jwt_auth_admin)):
    try:
        token = request.headers.get("Authorization")
        exact_token = token.split(" ")[1]
        await run_in_threadpool(SessionService.deleteSession, exact_token)
        return JSONResponse(
            content={
                "message": "logout successfully",
                "status": 200
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )

            
                    

        
        