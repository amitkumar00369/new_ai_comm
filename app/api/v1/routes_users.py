from fastapi import APIRouter
from app.controllers.user_controller import create_user,userLogin

userRouter: APIRouter = APIRouter()


userRouter.post("/create")(create_user)
userRouter.post("/login")(userLogin)