def process_voice_logic(text):
    if not text:
        return "I'm sorry, I couldn't hear anything clearly. Could you please repeat that?"

    text = text.lower()

    # Greeting
    if any(word in text for word in ["hello", "hi", "hey"]):
        return (
            "Hello! Thank you for calling. How may I assist you today? "
            "You can ask about our services, pricing, or make a booking."
        )

    # Pricing
    elif any(word in text for word in ["price", "cost", "charges", "fees"]):
        return (
            "Sure. Our services start from 999 rupees depending on your requirements. "
            "Would you like me to explain the available packages or help you with a booking?"
        )

    # Booking intent
    elif any(word in text for word in ["book", "appointment", "schedule", "reserve"]):
        return (
            "Great! I can help you with booking. "
            "Please tell me your preferred date and time, and I’ll check availability for you."
        )

    # Service inquiry
    elif any(word in text for word in ["service", "offer", "provide"]):
        return (
            "We offer a range of services tailored to your needs. "
            "Could you please specify what kind of service you are looking for?"
        )

    # Support / help
    elif any(word in text for word in ["help", "support", "issue", "problem"]):
        return (
            "I'm here to help you. Could you please describe your issue in more detail "
            "so I can assist you better?"
        )
    elif any(word in text for word in ["salon", "event", "restaurant"]):
        if "salon" in text:
            return (
                "We offer premium salon services including haircuts, styling, and spa treatments. "
                "Would you like to know more about our salon packages or make a booking?"
            )
        elif "event" in text:
            return (
                "Our event services include catering, decoration, and entertainment. "
                "Could you please specify the type of event you are planning?"
            )
        elif "restaurant" in text:
            return (
                "Our restaurant offers a variety of cuisines with a cozy ambiance. "
                "Would you like to know about our menu or make a reservation?"
            )
        return (
            "I'm here to help you. Could you please describe your issue in more detail "
            "so I can assist you better?"
        )

    # Fallback
    else:
        return (
            "I’m sorry, I didn’t fully understand that. "
            "You can ask about pricing, services, or say 'book' to make a reservation."
        )