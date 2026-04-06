# 🏠 Properties
properties = [
    {"id": 1, "title": "2BHK Flat in Noida", "price": 25000, "location": "Noida", "bedrooms": 2,"tenant_id": 1},
    {"id": 2, "title": "3BHK Flat in Delhi", "price": 40000, "location": "Delhi", "bedrooms": 3,"tenant_id": 3},
     {"id": 3, "title": "1BHK Flat in Noida", "price": 15000, "location": "Noida", "bedrooms": 1,"tenant_id": 2},
    {"id": 4, "title": "3BHK Flat in Delhi", "price": 40000, "location": "Delhi", "bedrooms": 3,"tenant_id": 1},
]

# 💇 Salons
salons = [
    {"id": 1, "name": "Luxury Salon", "service": "Haircut", "price": 500,"tenant_id": 1},
    {"id": 2, "name": "Style Hub", "service": "Facial", "price": 800,"tenant_id": 2},
       {"id": 3, "name": "Luxury Hub", "service": "Haircut", "price": 700,"tenant_id": 1},
    {"id": 4, "name": "Style Salon", "service": "Facial", "price": 900,"tenant_id": 3}
]

# 🎉 Events
events = [
    {"id": 1, "title": "Music Concert", "location": "Delhi", "price": 999,"tenant_id": 1},
    {"id": 2, "title": "Startup Meetup", "location": "Noida", "price": 499,"tenant_id": 2},
    {"id": 3, "title": "Tech Talk", "location": "Mumbai", "price": 299,"tenant_id": 3},
    {"id": 4, "title": "Art Exhibition", "location": "Bangalore", "price": 199,"tenant_id": 1},
    {"id": 5, "title": "Music Concert", "location": "Delhi", "price": 999,"tenant_id": 1},
    {"id": 6, "title": "Startup Meetup", "location": "Noida", "price": 499,"tenant_id": 2},
]


tenant_data = [
    {"id": 1, "tenant_id": 1, "name": "Aminata", "phone": "+14155238886", "email": "aminata@example.com","userType": "tenant","tenant_phone_number": "+918969172954", "services_provided": "property"},
    {"id": 2, "tenant_id": 1, "name": "John Doe", "phone": "+14155238887", "email": "john.doe@example.com","userType": "tenant","tenant_phone_number": "+9142657387464", "services_provided": "salon"},
    {"id": 3, "tenant_id": 2, "name": "Jane Smith", "phone": "+14155238888", "email": "jane.smith@example.com","userType": "tenant","tenant_phone_number": "+9142657387464", "services_provided": "event"}
]

# 📦 Leads (Booking Storage)
leads = []
def get_properties(tenant_id=None):
    if tenant_id is not None:
        return [p for p in properties if p["tenant_id"] == tenant_id]   
    return properties

def get_salons(tenant_id=None):
    if tenant_id is not None:
        return [s for s in salons if s["tenant_id"] == tenant_id]
    return salons

def get_events(tenant_id=None):
    if tenant_id is not None:
        return [e for e in events if e["tenant_id"] == tenant_id]
    return events