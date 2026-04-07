import stripe

from core.config import settings
import stripe
import time

# Set your secret key
stripe.api_key = settings.STRIPE_API_KEY


class StripeService:

    # -------------------- CUSTOMER --------------------
    def create_customer(self, payload):
        try:
            return stripe.Customer.create(
                description=payload.get("userName"),
                email=payload.get("email"),
                phone=payload.get("phone")
            )
        except Exception as e:
            raise e

    def retrieve_stripe_details(self, stripe_provider_id):
        try:
            return stripe.Account.retrieve(stripe_provider_id)
        except Exception as e:
            raise e

    # -------------------- CONNECT ACCOUNT --------------------
    def create_service_provider_account(self, payload):
        try:
            return stripe.Account.create(
                type="custom",
                email=payload["email"],
                business_type="individual",
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
                settings={
                    "payouts": {
                        "schedule": {"interval": "manual"}
                    }
                },
                business_profile={
                    "mcc": "5045",
                    "url": "https://www.jobdashflash.com/"
                },
                individual={
                    "first_name": payload["first_name"],
                    "last_name": payload["last_name"],
                    "email": payload["email"],
                    "phone": payload["phone"],
                    "dob": payload["dob"],
                    "address": {
                        "line1": payload["address"]["addressLine1"],
                        "city": payload["address"]["city"],
                        "state": payload["address"]["state"],
                        "country": payload["address"]["country"],
                        "postal_code": payload["address"]["zipCode"],
                    }
                },
                tos_acceptance={
                    "date": int(time.time()),
                    "ip": payload["ip"]
                }
            )
        except Exception as e:
            raise e

    def update_service_provider_profile(self, stripe_provider_id, payload):
        try:
            individual = {}

            if payload.get("socialSecurityNumber"):
                individual["id_number"] = payload["socialSecurityNumber"]
                individual["ssn_last_4"] = payload["socialSecurityNumber"][-4:]

            if payload.get("address"):
                individual["address"] = {
                    "line1": payload["address"]["addressLine1"],
                    "city": payload["address"]["city"],
                    "state": payload["address"]["state"],
                    "country": payload["address"]["country"],
                    "postal_code": payload["address"]["zipCode"],
                }

            if individual:
                return stripe.Account.modify(
                    stripe_provider_id,
                    individual=individual
                )
        except Exception as e:
            raise e

    # -------------------- CARD --------------------
    def create_card(self, customer_id, token):
        return stripe.Customer.create_source(
            customer_id,
            source=token
        )

    def delete_card(self, customer_id, card_id):
        return stripe.Customer.delete_source(customer_id, card_id)

    def update_card(self, customer_id, card_id, username):
        return stripe.Customer.modify_source(
            customer_id,
            card_id,
            name=username
        )

    # -------------------- BANK --------------------
    def generate_bank_account_token(self, payload):
        try:
            return stripe.Token.create(
                bank_account={
                    "country": payload["country"],
                    "currency": payload["currency"],
                    "account_holder_name": payload["userName"],
                    "account_holder_type": payload["account_holder_type"],
                    "routing_number": payload["routingNumber"],
                    "account_number": payload["accountNumber"],
                }
            )
        except Exception as e:
            raise e

    def create_bank_account(self, stripe_provider_id, token):
        return stripe.Account.create_external_account(
            stripe_provider_id,
            external_account=token
        )

    def update_bank_account(self, stripe_provider_id, bank_account_id, payload):
        return stripe.Account.modify_external_account(
            stripe_provider_id,
            bank_account_id,
            **payload
        )

    def delete_bank_account(self, stripe_provider_id, bank_account_id):
        return stripe.Account.delete_external_account(
            stripe_provider_id,
            bank_account_id
        )

    # -------------------- PAYMENTS --------------------
    def charge_payment(self, payload):
        try:
            return stripe.Charge.create(
                amount=int(float(payload["amount"]) * 100),
                currency="usd",
                customer=payload["customerId"],
                source=payload.get("source"),
                description="JOBDASHFLASH"
            )
        except Exception as e:
            raise e

    def create_payment_intent(self, payload):
        return stripe.PaymentIntent.create(
            amount=int(float(payload["amount"]) * 100),
            currency="usd",
            customer=payload["customerId"],
            payment_method_types=["card"],
            transfer_data={
                "destination": payload.get("destination")
            },
            application_fee_amount=int(float(payload.get("adminCommissionFee", 0)) * 100)
        )

    def confirm_payment_intent(self, payment_intent_id):
        return stripe.PaymentIntent.confirm(payment_intent_id)

    # -------------------- BALANCE --------------------
    def payment_balance_available(self, charge_id):
        charge = stripe.Charge.retrieve(charge_id)
        return stripe.BalanceTransaction.retrieve(charge.balance_transaction)

    def service_provider_balance(self, stripe_provider_id):
        return stripe.Balance.retrieve(stripe_account=stripe_provider_id)

    # -------------------- PAYOUT --------------------
    def create_payout(self, account_id, amount):
        return stripe.Payout.create(
            amount=int(float(amount) * 100),
            currency="usd",
            stripe_account=account_id
        )

    # -------------------- TRANSFER --------------------
    def transfer_payment(self, destination, amount, source=None):
        data = {
            "amount": int(float(amount) * 100),
            "currency": "usd",
            "destination": destination,
        }
        if source:
            data["source_transaction"] = source

        return stripe.Transfer.create(**data)

    # -------------------- WEBHOOK --------------------
    def create_webhook(self, url):
        return stripe.WebhookEndpoint.create(
            url=url,
            enabled_events=[
                "payout.canceled",
                "payout.created",
                "payout.failed",
                "payout.paid"
            ]
        )

    def listen_stripe_event(self, body, signature, secret):
        return stripe.Webhook.construct_event(
            body,
            signature,
            secret
        )

    # -------------------- DELETE --------------------
    def delete_customer(self, customer_id):
        return stripe.Customer.delete(customer_id)

    def delete_connected_account(self, account_id):
        return stripe.Account.delete(account_id)

    # -------------------- LIST --------------------
    def get_all_customer_ids(self):
        customers = stripe.Customer.list(limit=100)
        return [c.id for c in customers.data]

    def get_all_account_ids(self):
        accounts = stripe.Account.list(limit=100)
        return [a.id for a in accounts.data]


# Initialize service
stripe_service = StripeService()