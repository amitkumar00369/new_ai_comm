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
    return str(uuid.uuid4())

def generateSubscriptionId():
    return str(uuid.uuid4())

def generateMessageId():
    return str(uuid.uuid4())
def generateOtp():
    return random.randint(111111,999999)

