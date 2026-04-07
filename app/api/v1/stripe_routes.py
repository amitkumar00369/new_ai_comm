from fastapi import APIRouter
from app.controllers.stripe_controller import stripe_webhook,create_stripe_customer

stripeRouter: APIRouter = APIRouter()

stripeRouter.post("/status")(stripe_webhook)
stripeRouter.post("/create")(create_stripe_customer)