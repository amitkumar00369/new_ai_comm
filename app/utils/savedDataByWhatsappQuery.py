from app.utils.dummy_data import properties, salons, events


def extract_data_and_save_services(service_name, tenant_id, structure_data=None):
    if not structure_data:
        return "❌ No data provided"

    # 🏠 PROPERTY
    if service_name == "property":
        data = {
            "id": len(properties) + 1,
            "title": structure_data.get("name", "Unknown Property"),
            "price": structure_data.get("price", 0),
            "location": structure_data.get("location", "Unknown Location"),
            "bedrooms": structure_data.get("bedrooms", 0),
            "tenant_id": tenant_id
        }
        print("insert data:", data)
        properties.append(data)

        return f"🏠 Property saved: {data['title']} ₹{data['price']} ({data['location']})"

    # 💇 SALON
    elif service_name == "salon":
        data = {
            "id": len(salons) + 1,
            "name": structure_data.get("salon_name", "Unknown Salon"),
            "service": structure_data.get("salon_service", "Haircut"),
            "price": structure_data.get("salon_price", 0),
            "tenant_id": tenant_id
        }
        salons.append(data)

        return f"💇 Salon saved: {data['name']} - {data['service']} ₹{data['price']}"

    # 🎉 EVENT
    elif service_name == "event":
        data = {
            "id": len(events) + 1,
            "title": structure_data.get("event_title", "Unknown Event"),
            "location": structure_data.get("event_location", "Unknown Location"),
            "price": structure_data.get("event_price", 0),
            "tenant_id": tenant_id
        }
    
        events.append(data)

        return f"🎉 Event saved: {data['title']} ₹{data['price']} ({data['location']})"

    # ❌ UNKNOWN
    else:
        return f"❌ Unknown service: {service_name}"