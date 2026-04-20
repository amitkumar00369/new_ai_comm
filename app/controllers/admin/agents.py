from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi import Depends,Request
from app.middleware.auth_middleware import jwt_auth,jwt_auth_admin
from app.utils.enum import userType
from app.schemas.agentSchema import CreateAgent,AgentUpdate
from fastapi.concurrency import run_in_threadpool
from app.services.agentService import AgentService
from app.utils.constants import generateAgentId


async def createAgent(data: CreateAgent, admin = Depends(jwt_auth_admin)):
    try:
        payload = jsonable_encoder(data)
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
            "countryCode": payload["country_code"]
            
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
        
async def getAgents(admin = Depends(jwt_auth_admin)):
    try:
        agents = await run_in_threadpool(AgentService.getList)
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