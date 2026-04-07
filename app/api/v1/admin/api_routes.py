from fastapi import APIRouter
from app.controllers.admin.auth import create,login


adminRouter:APIRouter= APIRouter()

#  Authentication
adminRouter.post("/create")(create)
adminRouter.post("/login")(login)
