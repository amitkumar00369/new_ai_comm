
from enum import Enum

class RoomType(str, Enum):
    ONE_BHK = "0"
    TWO_BHK = "1"
    THREE_BHK = "2"
    FOUR_BHK = "3"

class userType(str, Enum):
    user="user"
    admin="admin"

class bookingType(str,Enum):
    pending = "0"
    accepted = "1"
    completed = "5",
    cancelled = "6",
    
    
class cmsType(str,Enum):
    aboutUs = "aboutUs"
    privacyPolicy = "privacyPolicy"
    termsAndConditions = "termsAndConditions"
    contactUse = "contactUs"
    
class souceType(str,Enum):
    call = "0"
    whatsapp = "1"
    
class senderType(str,Enum):
    user = "0"
    ai_agent= "1"

    
class paymentStatus(str,Enum):
    pending = "0"
    completed = "1"
    failed = "2"


class paymentMethod(str,Enum):
    card = "0"
    upi = "1"
    netbanking = "2"
    
class periodType(str,Enum):
    default = "0"  #24 hours plan will active
    monthly = "1"      # for one month  
    quaterly = "2"      # for three month
    yearly = "3"   # for one year
    
class planStatus(str,Enum):
    active = "0"
    expired = "1"
    
class planType(str,Enum):
    free = "0"
    paid = "1"
    
class bussinesType(str,Enum):
    it_services = "0"
    healthcare = "1"
    education = "2"
    finance = "3"
    retail = "4"
    real_estate = "5"
    hospitality = "6"
    manufacturing = "7"
    transportation = "8"
    event = "9"
    restaurants = "10"
    salon="11"
    
entity_keywords = {
    # "it_services": [
    #     "software", "website", "app", "development", "coding", "it", "tech",
    #     "api", "backend", "frontend", "bug", "server"
    # ],

    # "healthcare": [
    #     "doctor", "clinic", "hospital", "medicine", "appointment",
    #     "health", "checkup", "treatment", "dawai", "ilaj", "aspatal"
    # ],

    # "education": [
    #     "school", "college", "course", "class", "teacher", "coaching",
    #     "training", "study", "exam", "tuition", "subject"
    # ],

    # "finance": [
    #     "loan", "bank", "finance", "money", "investment", "emi",
    #     "insurance", "credit", "debit", "tax", "payment"
    # ],

    # "retail": [
    #     "shop", "store", "buy", "product", "price", "mall",
    #     "purchase", "order", "item", "sale"
    # ],

    # "real_estate": [
    #     "bhk", "flat", "apartment", "plot", "property", "rent",
    #     "buy house", "sell house", "villa", "land"
    # ],

    # "hospitality": [
    #     "hotel", "room", "stay", "booking", "resort",
    #     "guest house", "checkin", "checkout"
    # ],

    # "manufacturing": [
    #     "factory", "manufacturing", "production", "machine",
    #     "industrial", "assembly", "plant"
    # ],

    # "transportation": [
    #     "transport", "truck", "bus", "car", "delivery",
    #     "logistics", "shipment", "travel", "ride"
    # ],

    "event": [
        "movie", "cinema", "music", "game", "show",
        "concert", "fun", "event", "ticket"
    ],

    "restaurants": [
        "food", "restaurant", "menu", "order food", "eat",
        "dinner", "lunch", "breakfast", "cafe", "dish"
    ],

    "salon": [
        "salon", "haircut", "spa", "beauty", "makeup",
        "facial", "grooming", "parlor"
    ]
}