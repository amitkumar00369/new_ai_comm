import requests
from core.config import settings

def send_reply(to_number, message):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"

    result = requests.post(
        url,
        auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
        # data={
        #     "From": f"whatsapp:{settings.TWILIO_PHONE_NUMBER}",
        #     "To": to_number,
        #     "Body": message
        # },
        data = {
    "From": f"whatsapp:{settings.TWILIO_PHONE_NUMBER}",
    "To": to_number,
    "Body": message,
    "StatusCallback": "https://unsafetied-overfamiliar-kyra.ngrok-free.dev/api/v1/whatsapp/status"
}
    )
    if result.status_code == 201:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {result.text}")