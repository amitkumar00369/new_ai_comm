from fastapi import APIRouter
from app.controllers.user.user_controller import create_user,verifyOtp,editProfile

userRouter: APIRouter = APIRouter()


userRouter.post("/create")(create_user)
userRouter.post("/verifyOtp")(verifyOtp)
userRouter.put("/edit")(editProfile)