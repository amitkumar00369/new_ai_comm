from fastapi import APIRouter
from app.controllers.admin.auth import create,login,editProfile,logout
from app.controllers.admin.user import getUserList,blockUnblocked,deleleUser
from app.controllers.admin.plans import createPlan,updatePlan,getPlans,getPlansDetails
from app.controllers.admin.agents import createAgent,updateAgent,getAgents,getAgentDetails

adminRouter:APIRouter= APIRouter()

#  Authentication

adminRouter.post("/create")(create)
adminRouter.post("/login")(login)
adminRouter.get("/logout")(logout)
adminRouter.patch("/update")(editProfile)

adminRouter.post("/getUsers")(getUserList)
adminRouter.post("/blockUnblock/{id}")(blockUnblocked)
adminRouter.delete("/deleteUser/{id}")(deleleUser)



#  plan- create
adminRouter.post("/createPlan")(createPlan)
adminRouter.patch("/updatePlan")(updatePlan)
adminRouter.get("/getPlans")(getPlans)
adminRouter.get("/getPlansDetails/{id}")(getPlansDetails)


# Create agent
adminRouter.post("/create-agent")(createAgent)
adminRouter.patch("/updateAgent")(updateAgent)
adminRouter.get("/getAgents")(getAgents)
adminRouter.get("/getAgentDetails/{id}")(getAgentDetails)



