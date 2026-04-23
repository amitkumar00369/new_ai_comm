import random
import uuid

def generateUserId():
    return str(uuid.uuid4())

def generateTenantId():
    return str(uuid.uuid4())

def generateLeadId():
    return str(uuid.uuid4())

def generateCallId():
    return str(uuid.uuid4())

def generatePlanId():
    return "plan"+ str(random.randint(11111,99999))

def generateSubscriptionId():
    return "subs"+ str(random.randint(11111,99999))

def generateMessageId():
    return str(uuid.uuid4())
def generateOtp():
    return random.randint(111111,999999)

def generateLeadId(phone_number):
    return phone_number +"lead"+ str(random.randint(111111,999999))

def generateAgentId(name):
    return name + str(random.randint(1111,9999))
    

