from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi import Depends,Request
from app.services.plan_service import PlanService
from app.middleware.auth_middleware import jwt_auth,jwt_auth_admin
from app.utils.enum import userType
from app.schemas.agentSchema import CreateAgent,AgentUpdate
from fastapi.concurrency import run_in_threadpool
from app.services.agentService import AgentService
from app.utils.constants import generateAgentId


async def createAgent(data: CreateAgent, admin = Depends(jwt_auth_admin)):
    try:
        payload = jsonable_encoder(data)
        isPlanActive = await run_in_threadpool(PlanService.findById, payload.get("plan_id"))
        if isPlanActive is None:
            return JSONResponse(content={
                "message": "Plan not active",
                "'status": 400
            },status_code=400)
        findAgentWithThisNumber = await run_in_threadpool(AgentService.findByNumber,payload["phone_number"])
        if findAgentWithThisNumber:
            return JSONResponse(content={
                "message": "You have already agent with this number",
                "status": 400
            },status_code=400)
        isagentExist = await run_in_threadpool(
                    AgentService.findByName,
                    payload.get("name")
                )
        if isagentExist:
            return JSONResponse(content={
                "message": "You have already agent with this name",
                "status": 400
            },status_code=400)
        createPayload = {
            "agentWhatsappNumber": payload["phone_number"],
            "agentId": await run_in_threadpool(generateAgentId, payload["name"]),
            "name":  payload["name"],
            "countryCode": payload["country_code"],
            "plan_id": payload.get("plan_id")
            
        }
        agent = await run_in_threadpool(AgentService.create, createPayload)
        
        return JSONResponse(content={
            "message":"Agent created successfully",
            "data": agent,
            "status": 200
        })
    except Exception as e:
        return JSONResponse(
            content={
                "message": "Intrenal server error",
                "status": 500
            },status_code=500
        )
async def updateAgent(data: AgentUpdate,admin = Depends(jwt_auth_admin)):
    try:
        
        payload = jsonable_encoder(data)
        agent = await run_in_threadpool(AgentService.findById, payload.get("id"))
        if not agent:
            return JSONResponse(content={
                "message": "Agent not find",
                "status": 404
            },status_code=404)
     
    
        payloadData = {}
        message = ""
        if payload.get("type")=="2":   # for block unblock
            if agent.get("isBlocked"):
                payloadData["isBlocked"] = False
                message = "Agent unblocked successfully"
            else:
                payloadData["isBlocked"] = True
                message = "Agent blocked successfully"
        elif payload.get("type")=="3":    # for delete
            payloadData["isDeleted"] = True
            message = "Agent has been deleted successfully"
            
        elif payload.get("type") == "1":  # update profile
    
            if payload.get("name"):
                
                isagentExist = await run_in_threadpool(
                    AgentService.findByName,
                    payload.get("name")
                )

                # Case 1: No agent found → safe to update
                if isagentExist is None:
                    payloadData["name"] = payload.get("name")

                else:
                    # Case 2: Same agent (same ID) → allow
                    if isagentExist.get("id") == payload.get("id"):
                        payloadData["name"] = payload.get("name")

                    # Case 3: Different agent with same name → reject
                    else:
                        return JSONResponse(
                            content={
                                "message": "Agent already exist",
                                "status": 400
                            },
                            status_code=400
                        )

            # print("asdfgh", payloadData)
            if payload.get("plan_id"):
                isPlanActive = await run_in_threadpool(PlanService.findById, payload.get("plan_id"))
                if isPlanActive is None:
                    return JSONResponse(content={
                        "message": "Plan not active",
                        "'status": 400
                    },status_code=400)
                
                                                    
                payloadData["plan_id"] =  payload.get("plan_id")

        

            print("payload", payloadData)

            message = "agent updated successfully"
        else:
            return JSONResponse(content={
                "message": "Invalid types",
                "status": 400
            },status_code=400)
        print("djfjfjfj",agent)
        agentData=  await run_in_threadpool(AgentService.agentUpgrade,agent.get("id"), payloadData)
        return JSONResponse(content={
            "message": message,
            "data": agentData,
            "status": 200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        
async def getAgents(data: dict, request: Request,admin = Depends(jwt_auth_admin)):
    try:
        query = {
            "page": int(request.query_params.get("page", 1)),
            "limit": int(request.query_params.get("limit",10))
        }
        payload = jsonable_encoder(data)
        agents = await run_in_threadpool(AgentService.getList,payload,query)
        return JSONResponse(content={
            "message": "success",
            "data": agents or [],
            "status":  200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
async def getAgentsByUsers(data: dict,request: Request,admin = Depends(jwt_auth)):
    try:
        query = {
            "page": int(request.query_params.get("page", 1)),
            "limit": int(request.query_params.get("limit",10))
        }
        payload = jsonable_encoder(data)
        agents = await run_in_threadpool(AgentService.getListByUser,payload,query)
        return JSONResponse(content={
            "message": "success",
            "data": agents or [],
            "status":  200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
async def getAgentDetails(id: int,admin = Depends(jwt_auth_admin)):
    try:
        agents = await run_in_threadpool(AgentService.findById, id)
        return JSONResponse(content={
            "message": "success",
            "data": agents or [],
            "status":  200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        
async def assignAgents(id, user = Depends(jwt_auth)):
    try:
        agent = await run_in_threadpool(AgentService.findById, id)
        if agent.get("isAssigned"):
            return JSONResponse(content={
                "message": "Agent already assinged",
                "status": 400
            },status_code=400)
        if agent.get("isBlocked"):
            return JSONResponse(content={
                "message": "Agent has blocked",
                "status": 400
            },status_code=400)
        if agent.get("isDeleted"):
            return JSONResponse(content={
                "message": "Agent has deleted",
                "status": 400
            },status_code=400)
        updateData = {
            "assignedBy": user.get("id"),
            "isAssigned" : True
        }
        agentData = await run_in_threadpool(AgentService.agentUpgrade,agent.get("id"), updateData)
        return JSONResponse(content={
            "message": "success",
            "data": agentData or [],
            "status":  200
        },status_code=200)
    except Exception as e:
        return JSONResponse(content={
            "message": "Internal server error",
            "err": str(e),
            "status": 500
        },status_code=500)
        