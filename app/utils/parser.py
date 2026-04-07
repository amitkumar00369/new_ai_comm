import re

def parse_message(message: str):
    msg = message.lower()
    print("Parsing message:", msg)

    # 🔥 Intent
    if "book" in msg or "appointment" in msg:
        intent = "booking"
    elif "price" in msg:
        intent = "price_inquiry"
    elif "available" in msg or "availability" in msg or "available hai" in msg or "list" in msg or "give" in msg or "show" in msg:
        print("Intent: Search")
        intent = "search"
    elif "hi" in msg or "hello" in msg or "hey" in msg or "hii" in msg or "great" in msg or "good" in msg or "awesome" in msg or "well" in msg or "okay" in msg:
        intent = "greeting"
    else:
        intent = "unknown"

    # 🔥 Entity
    if "salon" in msg or "haircut" in msg:
        entity = "salon"
    elif "bhk" in msg or "flat" in msg:
        entity = "property"
    elif "event" in msg:
        entity = "event"
    else:
        entity = "general"
    # location extract    location = None
    if "noida" in msg:
        location = "Noida"
    elif "delhi" in msg:
        location = "Delhi"
    elif "mumbai" in msg:
        location = "Mumbai"
    elif "bangalore" in msg:
        location = "Bangalore"
    else:
        location = None
    # service extract
    if "haircut" in msg:
        service = "Haircut"
    elif "facial" in msg:
        service = "Facial"
    else:
        service = None


    # 🔥 Price extract
    price = None
    numbers = re.findall(r"\d+(?!\s*bhk)", msg)  # Find numbers not followed by "bhk"
    if numbers:
        price = int(numbers[0])
        
    # find the name of property, salon or event
    name = None
    if entity == "property":
        name_match = re.search(r"(\d+bhk\s\w+)", msg)
        if name_match:
            name = name_match.group(1)
    elif entity == "salon":
        name_match = re.search(r"(luxury salon|style hub|luxury hub|style salon)", msg)
        if name_match:
            name = name_match.group(1)
    elif entity == "event":
        name_match = re.search(r"(music concert|startup meetup|tech talk|art exhibition)", msg)
        if name_match:
            name = name_match.group(1)
    # find number of bedrooms for property
    bedrooms = None
    if entity == "property":
        bedrooms_match = re.search(r"(\d+)bhk", msg)
        if bedrooms_match:
            bedrooms = int(bedrooms_match.group(1))

    return {
        "intent": intent,
        "entity": entity,
        "price": price,
        "location": location,
        "service": service,
        "name": name,
        "bedrooms": bedrooms
    }   
   
   