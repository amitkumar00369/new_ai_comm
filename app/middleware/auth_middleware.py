from fastapi import Request, HTTPException
from starlette.concurrency import run_in_threadpool
from ..services.sessionService import SessionService
from ..services.user_service import userService


async def jwt_auth(request: Request):
    # print(request.headers)

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=400, detail="Authorization header missing")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Bearer token format")

    exact_token = token.split(" ")[1]
    # print(exact_token)

    is_token_exist = await run_in_threadpool(SessionService.getSessionData, exact_token)
    if is_token_exist is None:
        raise HTTPException(status_code=404, detail="Token not found")

    decoded = SessionService.decodeSession(exact_token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Unauthorized token")

    user = await run_in_threadpool(userService.findById, decoded)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    request.state.user = user
    return user
