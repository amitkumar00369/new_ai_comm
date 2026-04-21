from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi import Depends,Request
from app.middleware.auth_middleware import jwt_auth,jwt_auth_admin
from app.utils.constants import  generatePlanId
from app.utils.enum import userType
from app.schemas.planSchema import create,PlanUpdate
from fastapi.concurrency import run_in_threadpool
from app.services.plan_service import PlanService


async def createPlan(data: create,admin = Depends(jwt_auth_admin)):
    try:
        
        payload = jsonable_encoder(data)
        payload["planId"] = await run_in_threadpool(generatePlanId)
        plan = await run_in_threadpool(PlanService.findByName,payload.get("name"))
        if plan:
            return JSONResponse(content={
                "message": "Plan already exist",
                "status": 400
            },status_code=400)
        planData=  await run_in_threadpool(PlanService.create,payload)
        return JSONResponse(content={
            "message":"plan created",
            "data": planData,
            "status": 200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        
async def updatePlan(data: PlanUpdate,admin = Depends(jwt_auth_admin)):
    try:
        
        payload = jsonable_encoder(data)
        plan = await run_in_threadpool(PlanService.findById, payload.get("id"))
        if not plan:
            return JSONResponse(content={
                "message": "Plan not find",
                "status": 404
            },status_code=404)
        payloadData = {}
        message = ""
        if payload.get("type")=="2":   # for block unblock
            if plan.get("isBlocked"):
                payloadData["isBlocked"] = False
                message = "Plan unblocked successfully"
            else:
                payloadData["isBlocked"] = True
                message = "Plan blocked successfully"
        elif payload.get("type")=="3":    # for delete
            payloadData["isDeleted"] = True
            message = "Plan has been deleted successfully"
            
        elif payload.get("type") == "1":  # update profile
    
            if payload.get("name"):
                
                isPlanExist = await run_in_threadpool(
                    PlanService.findByName,
                    payload.get("name")
                )

                # Case 1: No plan found → safe to update
                if isPlanExist is None:
                    payloadData["name"] = payload.get("name")

                else:
                    # Case 2: Same plan (same ID) → allow
                    if isPlanExist.get("id") == payload.get("id"):
                        payloadData["name"] = payload.get("name")

                    # Case 3: Different plan with same name → reject
                    else:
                        return JSONResponse(
                            content={
                                "message": "Plan already exist",
                                "status": 400
                            },
                            status_code=400
                        )
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
            print("asdfgh", payloadData)

            payloadData["planType"] = payload.get("planType")
            payloadData["period"] = payload.get("period")
            payloadData["price"] = payload.get("price")

            print("payload", payloadData)

            message = "Plan updated successfully"
        else:
            return JSONResponse(content={
                "message": "Invalid types",
                "status": 400
            },status_code=400)
        print("djfjfjfj",plan)
        planData=  await run_in_threadpool(PlanService.planUpgrade,plan.get("id"), payloadData)
        return JSONResponse(content={
            "message": message,
            "data": planData,
            "status": 200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        
async def getPlans(data: dict, request: Request,admin = Depends(jwt_auth_admin)):
    try:
        query = {
            "page": int(request.query_params.get("page", 1)),
            "limit": int(request.query_params.get("limit",10))
        }
        payload = jsonable_encoder(data)
        plans = await run_in_threadpool(PlanService.getList,payload,query)
        return JSONResponse(content={
            "message": "success",
            "data": plans or [],
            "status":  200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
async def getPlansDetails(id: int,admin = Depends(jwt_auth_admin)):
    try:
        plans = await run_in_threadpool(PlanService.findById, id)
        return JSONResponse(content={
            "message": "success",
            "data": plans or [],
            "status":  200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)