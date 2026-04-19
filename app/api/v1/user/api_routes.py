from fastapi import APIRouter
from app.controllers.user.user_controller import create_user,verifyOtp,editProfile, login,logout,deleteAccount,resentOtp
from app.controllers.user.tenant_controller import createTenat,getTenatDetails
userRouter: APIRouter = APIRouter()

# User Auhtentication apis

userRouter.post("/create")(create_user)
userRouter.post("/login")(login)
userRouter.post("/verifyOtp")(verifyOtp)
userRouter.post("/sentOtp")(resentOtp)
userRouter.put("/edit")(editProfile)
userRouter.get("/logout")(logout)
userRouter.delete("/delete")(deleteAccount)

# tenant api
userRouter.post("/create-tenat")(createTenat)
userRouter.post("/get-tenat")(getTenatDetails)

