from fastapi import Request, HTTPException
from starlette.concurrency import run_in_threadpool

from app.utils.enum import userType
from ..services.sessionService import SessionService
from ..services.user_service import userService
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from starlette.concurrency import run_in_threadpool
from app.services.sessionService import SessionService
from app.services.user_service import UserService


async def jwt_auth(request: Request):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Bearer token format")

    exact_token = token.split(" ")[1]

    # ✅ Check token exists in DB
    session = await run_in_threadpool(
        SessionService.getSessionData,
        exact_token
    )

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # ✅ Decode token
    try:
        decoded = SessionService.decodeSession(exact_token)
        print("dhbfhb",decoded)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    # ✅ Get user
    user = await run_in_threadpool(
        UserService.findById,
        decoded
    )
    print("users",user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Attach user to request
    request.state.user = user

    return user



async def jwt_auth_admin(request: Request):
    token = request.headers.get("Authorization")

    if not token:
       raise HTTPException(status_code=401, detail="Authorization header missing")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Bearer token format")

    exact_token = token.split(" ")[1]

    # ✅ Check token exists in DB
    session = await run_in_threadpool(
        SessionService.getSessionData,
        exact_token
    )

    if not session:
       raise HTTPException(status_code=401, detail="Invalid or expired token")

    # ✅ Decode token
    try:
        decoded = SessionService.decodeSession(exact_token)
        print(decoded)
    except Exception:
       raise HTTPException(status_code=401, detail="Invalid token")

    # ✅ Get user
    user = await run_in_threadpool(
        UserService.findById,
        decoded
    )
    if user["userType"]!=userType.admin:
        raise HTTPException(status_code=400, detail="You are not allow to access")
        
    print("usersssssss",user)
    if not user:
       raise HTTPException(status_code=404, detail="User not found")

    # ✅ Attach user to request
    request.state.user = user

    

    return user