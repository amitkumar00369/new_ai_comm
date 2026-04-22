from ast import parse
import struct

from alembic.util import msg
from fastapi.concurrency import run_in_threadpool
from requests import get
from app.utils.enum import bussinesType
from app.utils import whatsapp
from app.utils.dummy_data import get_properties, get_salons, get_events,tenant_data
from app.services.tenant_service import TenatService
from app.services.agentService import AgentService
from app.services.bussiness_service import BussinessService
from app.services.lead_service import create_lead
from app.utils.savedDataByWhatsappQuery import extract_data_and_save_services
from app.utils.parser import parse_message
from app.utils.redis_session import save_session,get_session,get_last_message


                
                
def find_tenant_or_user_by_number(user_msg, tenant_number=None, sender_number=None):

    # normalize numbers
    sender_number = sender_number.split(":")[1] if sender_number and sender_number.startswith("whatsapp") else None
    tenant_number = tenant_number.split(":")[1] if tenant_number and tenant_number.startswith("whatsapp") else None

    agentNumber = tenant_number[3:]
    leadNumber = sender_number[3:]

    agentData = AgentService.findByNumberWithUserDetails(agentNumber)
    session_id = f"{sender_number}:{tenant_number}"

    nor_msg = parse_message(user_msg)

    if not agentData:
        return "Agent not found"

    agentDatas = agentData.get("agent")
    ownerDatas = agentData.get("user")
    tenantDatas = agentData.get("tenant")

    #  GET SESSION
    session = get_session(session_id) or {
        "sender_number": sender_number,
        "agent_number": tenant_number,
        "messages": []
    }

    # ADD USER MESSAGE
    session["messages"].append({
        "sender": "user",
        "message": user_msg,
        
    })

    # OWNER CASE
    if ownerDatas['phone_number'] == leadNumber:
        bussinessName = bussinesType(tenantDatas.get("bussiness_name")).name

        reply = f"You are owner of {bussinessName} service"

    else:
        # HANDLE NORMAL USER FLOW
        lastMessage = get_last_message(session_id)
        print(lastMessage)
        reply = handle_message(user_msg, sender_number, ownerDatas, tenantDatas, agentDatas)

    #  ADD BOT REPLY
    session["messages"].append({
        "sender": "bot",
        "message": reply
    })

    # STORE EXTRA DATA
    session["last_intent"] = nor_msg["intent"]
    session["last_entity"] = nor_msg["entity"]
    session["normalize_message"] = nor_msg

    #  SAVE ONCE (IMPORTANT)
    save_session(session_id, session)

    return reply
      
        
            

    



def format_list(data, entity):
    bussinessName = bussinesType(entity).name

    if not data:
        return {
            "message": """😅 No services found

👉 Try another location  
👉 Or type "menu"
""",
            "mapping": {}
        }

    msg = "Here are available services 👇\n\n"
    mapping = {}

    numbers = []   # 👈 dynamic numbers collect karne ke liye

    for i, item in enumerate(data, 1):
        msg += f"""{i}️⃣ {item['title']}
📍 {item['location']} | 💰 ₹{item['price']}

"""
        mapping[str(i)] = item["id"]
        numbers.append(str(i))   # 👈 collect numbers

    # 🔥 dynamic join
    number_text = " / ".join(numbers)

    msg += f"""👉 Reply *{number_text}* to book  
👉 Or type service name (e.g. {bussinessName})  
👉 Type "menu" to restart
"""

    return msg


# 🔥 MAIN FUNCTION (THIS WAS MISSING)
def handle_message(user_msg, user_number,ownerData,tenantData,agentData):
    # print(tenantData,agentData,ownerData)
    serviceType = tenantData.get("business_name")
    bussinessName = bussinesType(tenantData.get("business_name")).name
    

    nor_msg = parse_message(user_msg)
    print("Parsed Message:", nor_msg)
    intent = nor_msg['intent']
    entity = nor_msg['entity']
    print("Intent:", intent, "Entity:", entity,"serviceType",serviceType,"bussinessName",bussinessName)
    

    # GREETING
    if intent == "greeting" and entity == "general":
        if  "great" in user_msg.lower() or "good" in user_msg.lower() or "awesome" in user_msg.lower() or "well" in user_msg.lower() or "ok" in user_msg.lower():
            return "Thats awesome! How can I help you?"
        return f"Hello 👋! How can I help you? I am {agentData.get('name')}: {bussinessName} service provider"

    #  SEARCH FLOW
    if intent == "search":
        # supose user has sent message give me list then i knew that from whict tenant number we message while 
        # currenly using property provider then we reply message with greeting this is ur service list
        if  entity == "general" and serviceType== bussinesType.real_estate:
            data = BussinessService.findByUserId(ownerData["id"])

            return format_list(data, serviceType)
        if entity == bussinessName  and serviceType== bussinesType.real_estate:
            data = []
            if nor_msg['location'] is not None:
                data = [p for p in BussinessService.findByUserId(ownerData["id"]) if p['location'].lower() == nor_msg['location'].lower()]
            else:
                data = BussinessService.findByUserId(ownerData["id"])
            return format_list(data, serviceType)
        if entity == "general" and serviceType== bussinesType.healthcare:
            print("yessss ")
            data = BussinessService.findByUserId(ownerData["id"])
            # print("wrong here",data)
            return format_list(data, serviceType)
        if entity == bussinessName and  serviceType== bussinesType.healthcare:
            data = []
            if nor_msg['location'] is not None:
                data = [p for p in BussinessService.findByUserId(ownerData["id"]) if p['location'].lower() == nor_msg['location'].lower()]
            else:
                data = BussinessService.findByUserId(ownerData["id"])
            return format_list(data, serviceType)
        if  entity == "general" and serviceType== bussinesType.salon:
            data = BussinessService.findByUserId(ownerData["id"])

            return format_list(data, serviceType)

        elif entity == bussinessName and serviceType== bussinesType.salon:
            data = []
            
            if nor_msg['service'] is not None:
                data = [s for s in BussinessService.findByUserId(ownerData["id"]) if s['service'].lower() == nor_msg['service'].lower()]
            else:
                data = BussinessService.findByUserId(ownerData["id"])
            return format_list(data, serviceType)

        elif entity == bussinessName and  entity == "general" and serviceType== bussinesType.entertainment:
            data = []
            if nor_msg['location'] is not None:
                data = [e for e in BussinessService.findByUserId(ownerData["id"])  if e['location'].lower() == nor_msg['location'].lower()]
            else: 
                data =BussinessService.findByUserId(ownerData["id"])
            # data = get_events()
            return format_list(data, serviceType)

        else:
            return f" 😊 I m provider {agentData['name']} and i provide {bussinessName} services"

    # 🟢 PRICE
    if intent == "price_inquiry":
            data = []
            if nor_msg['location'] is not None and nor_msg['price'] is not None :
                data = [p for p in BussinessService.findByUserId(ownerData["id"]) if p['location'].lower() == nor_msg['location'].lower() and p['price'] < nor_msg['price'] ]
            if nor_msg['location'] is not None:
                data = [p for p in BussinessService.findByUserId(ownerData["id"]) if p['location'].lower() == nor_msg['location'].lower()]
            elif nor_msg['price'] is not None:
                data = [p for p in BussinessService.findByUserId(ownerData["id"]) if p['price']< nor_msg['price']]
            else:
                data =BussinessService.findByUserId(ownerData["id"])
            if data:
                msg = format_list(data,serviceType)
                # min_price = min([p['price'] for p in data])
                return f" Here are services\n: {msg}"
       
       
    if intent == "booking":
     
        return handle_booking(nor_msg, user_number, agentData,ownerData,tenantData)
        

    #  BOOKING
def handle_booking(nor_msg, user_number, agentData,ownerData,tenantData):
        serviceType = tenantData.get("business_name")
        bussinessName = bussinesType(tenantData.get("business_name")).name
        lead = None
        if nor_msg['entity'] == "general":
            data = BussinessService.findByUserId(ownerData["id"])

            msg = format_list(data, serviceType)
            return f"Reply with number or service name to book.\n {msg}"
        if nor_msg['entity'] == bussinessName and serviceType == bussinesType.healthcare:
            
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