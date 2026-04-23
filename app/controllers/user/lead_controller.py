
from typing import Optional

from fastapi.params import Depends

from app.middleware.auth_middleware import jwt_auth
from app.services.lead_service import get_leads_by_user_id

from ...services.user_service import UserService
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


async def getLeadData(user = Depends(jwt_auth)):
    try:
        leadData = await run_in_threadpool(get_leads_by_user_id, user.get("id"))
        return JSONResponse(content={"status":200, "message": "Lead data fetched successfully", "data": leadData},status_code=200)
    except Exception as e:
        return JSONResponse(content={"status":500, "message": "An error occurred while fetching lead data"},status_code=500)