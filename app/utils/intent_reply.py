from ast import parse
import struct

from alembic.util import msg
from requests import get

from app.utils import whatsapp
from app.utils.dummy_data import get_properties, get_salons, get_events,tenant_data
from app.services.lead_service import create_lead
from app.utils.savedDataByWhatsappQuery import extract_data_and_save_services
from app.utils.parser import parse_message

def find_tenant_or_user_by_number(user_msg, tenant_number=None, sender_number=None):
    # whatsapp:+14155238886
    sender_number = sender_number.split(":")[1] if sender_number and sender_number.split(":")[0] == "whatsapp" else None
    tenant_number = tenant_number.split(":")[1] if tenant_number and tenant_number.split(":")[0] == "whatsapp" else None
    print("Looking for tenant with phone:", tenant_number, "and sender number:", sender_number)

    for tenant in tenant_data:
        if tenant['phone'] == tenant_number:
            # if tenant["tenant_phone_number"] == sender_number:
            #     return "Aap tenant ho, aap apne services data bhej sakte ho jisse main aapke liye leads create kar saku!"
            #     nor_msg = parse_message(user_msg)
            #     print("normalized message for tenant:", nor_msg )
            #     data = extract_data_and_save_services(tenant["services_provided"], tenant["tenant_id"], structure_data=nor_msg)
            #     # print("Tenant found:", tenant) and this message will be extarcted and save into his services data like property,salon, event etc  
            #     return f"You are only sent data to prepare you services data  to add!\n: {data}"
            # else:
            data = handle_message(user_msg, sender_number, tenant_number,tenant)
            return data

    



def format_list(data, entity):
    msg = ""

    if entity == "property":
        for item in data:
            msg += f"🏠 {item['title']} - ₹{item['price']}\n"

    elif entity == "salon":
        for item in data:
            msg += f"💇 {item['name']} - {item['service']} ₹{item['price']}\n"

    elif entity == "event":
        for item in data:
            msg += f"🎉 {item['title']} - ₹{item['price']}\n"

    return msg


# 🔥 MAIN FUNCTION (THIS WAS MISSING)
def handle_message(user_msg, user_number,tenant_number,tenant):

    nor_msg = parse_message(user_msg)
    print("Parsed Message:", nor_msg)
    intent = nor_msg['intent']
    entity = nor_msg['entity']
    print("Intent:", intent, "Entity:", entity)
    

    # 🟢 GREETING
    if intent == "greeting" and entity == "general":
        if  "great" in user_msg.lower() or "good" in user_msg.lower() or "awesome" in user_msg.lower() or "well" in user_msg.lower() or "ok" in user_msg.lower():
            return "Thats awesome! How can I help you?"
        return f"Hello 👋! How can I help you? I am {tenant['name']}: {tenant['services_provided']} service provider"

    # 🟢 SEARCH FLOW
    if intent == "search":
        # supose user has sent message give me list then i knew that from whict tenant number we message while 
        # currenly using property provider then we reply message with greeting this is ur service list
        if entity == "general" and tenant["services_provided"] == "property":
            data = get_properties(tenant["tenant_id"])
            return format_list(data, "property")
        if entity == "property" and tenant["services_provided"] == "property":
            data = []
            if nor_msg['location'] is not None:
                data = [p for p in get_properties(tenant["tenant_id"]) if p['location'].lower() == nor_msg['location'].lower()]
            else:
                data = get_properties(tenant["tenant_id"])
            return format_list(data, entity)

        elif entity == "salon" and tenant["services_provided"] == "salon":
            data = []
            
            if nor_msg['service'] is not None:
                data = [s for s in get_salons(tenant["tenant_id"]) if s['service'].lower() == nor_msg['service'].lower()]
            else:
                data = get_salons(tenant["tenant_id"])
            return format_list(data, entity)

        elif entity == "event" and tenant["services_provided"] == "event":
            data = []
            if nor_msg['location'] is not None:
                data = [e for e in get_events(tenant["tenant_id"]) if e['location'].lower() == nor_msg['location'].lower()]
            else: 
                data = get_events(tenant["tenant_id"])
            # data = get_events()
            return format_list(data, entity)

        else:
            return f" 😊 I m provider {tenant['name']} and i provide {tenant['services_provided']} services"

    # 🟢 PRICE
    if intent == "price_inquiry":

        if tenant["services_provided"] == "property":
                data = []
                if nor_msg['location'] is not None:
                    data = [p for p in get_properties(tenant["tenant_id"]) if p['location'].lower() == nor_msg['location'].lower()]
                else:
                    data = get_properties(tenant["tenant_id"])
                if data:
                    min_price = min([p['price'] for p in data])
                    return f"💰 Property prices start from ₹{min_price}"
       
        if tenant["services_provided"] == "salon":
            data = []
            if nor_msg['service'] is not None:
                data = [s for s in get_salons(tenant["tenant_id"]) if s['service'].lower() == nor_msg['service'].lower()]
            else:
                data = get_salons(tenant["tenant_id"])
            if data:
                min_price = min([s['price'] for s in data])
                return f"💰 Salon prices start from ₹{min_price}"
        if tenant["services_provided"] == "event":
            data = []
            if nor_msg['location'] is not None:
                data = [e for e in get_events(tenant["tenant_id"]) if e['location'].lower() == nor_msg['location'].lower()]
            else:
                data = get_events(tenant["tenant_id"])
            if data:
                min_price = min([e['price'] for e in data])
                return f"💰 Event prices start from ₹{min_price}"
    if intent == "booking":
        return handle_booking(nor_msg, user_number, tenant_number,tenant)
        

    # 🟢 BOOKING
def handle_booking(nor_msg, user_number, tenant_number,tenant):
        lead = None
        if nor_msg['entity'] == "general":
            return "Kya book karna hai? (property/salon/event)"
        if nor_msg['entity'] == "property" and tenant["services_provided"] == "property":
            item_id = 1  # For simplicity, we are hardcoding the item_id
            data = get_properties(tenant["tenant_id"])
            if  nor_msg.get('price') is None:
                return "💰 Price is required for booking a property"
            if nor_msg.get("location") is None:
                return " Location is required for booking a property"
            if nor_msg.get('price') is not None and nor_msg.get('location') is not None:
                data = [p for p in get_properties(tenant["tenant_id"]) if p['price'] == nor_msg.get('price') or p['location'].lower() == nor_msg.get('location').lower()]
            if data:
                item_id = data[0]['id']
            lead = create_lead(user_number, nor_msg['entity'], item_id, tenant_number=tenant_number, tenant_id=tenant["id"])
            return f"✅ Booking has been confirmed !\nLead: {lead}"
        if nor_msg['entity'] == "salon" and tenant["services_provided"] == "salon":
            data = get_salons(tenant["tenant_id"])
            item_id = None
            if not nor_msg.get('price'):
                return "💰 Price is required for booking a salon"

            if nor_msg.get("service") is None:
                return "Service type is required for booking a salon"
            if nor_msg.get('price') is not None and nor_msg.get('service') is not None:
                data = [s for s in get_salons(tenant["tenant_id"]) if s['price'] == nor_msg.get('price') and s['service'].lower() == nor_msg.get('service').lower()]
            if data:
                item_id = data[0]['id']
          
            lead = create_lead(user_number, nor_msg['entity'], item_id, tenant_number=tenant_number)
            return f"✅ Booking has been confirmed !\nLead: {lead}"
        if nor_msg['entity'] == "event" and tenant["services_provided"] == "event":
            item_id = None
            data = get_events(tenant["tenant_id"])
            if not nor_msg.get('price'):
                return "💰Price is required for booking an event"
            if nor_msg.get("location") is None:
                return "Location is required for booking an event"

            if nor_msg.get('price') is not None and nor_msg.get('location') is not None:
                data = [e for e in get_events(tenant["tenant_id"]) if e['price'] == nor_msg.get('price') or e['location'].lower() == nor_msg.get('location').lower()]
            if data:
                item_id = data[0]['id']
            lead = create_lead(user_number, nor_msg.get('entity'), item_id, tenant_number=tenant_number)

            return f"✅ Booking has been confirmed !\nLead: {lead}"

    # 🟢 AVAILABILITY
        # if nor_msg['intent'] == "availability":
        #     return "✅ Available hai"
        return "I don't understand 😅"