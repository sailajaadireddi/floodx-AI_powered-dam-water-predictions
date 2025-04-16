from geopy.distance import geodesic
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

twilio_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE")

client = Client(twilio_sid, auth_token)import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('app.log')
stream_handler = logging.StreamHandler()

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Capitol Hotel location (change this if needed)
capitol_hotel_location = (17.6868, 83.2185)

# Friends' updated location to Capitol Hotel
friends = [
    {"name": "Praneetha", "phone": "‪+918074474677‬", "loc": capitol_hotel_location, "zone": "Green Zone"},  # Set to Capitol Hotel
    {"name": "hema", "phone": "‪+918328611819‬", "loc": capitol_hotel_location, "zone": "Green Zone"},    # Set to Capitol Hotel
    ]

def send_alert_to_capitol_hotel():
    logger.info("Sending Alerts to Capitol Hotel contacts...")
    for f in friends:
        if f["loc"] == capitol_hotel_location:  # Only send messages to Capitol Hotel location
            distance = geodesic(capitol_hotel_location, f["loc"]).meters
            if distance <= 3000:  # Only send messages to those within 3 km of Capitol Hotel
                msg = f"Hi {f['name']}! Your area is under a GREEN ZONE Alert. The dam storage levels are safe, but stay alert and prepared for any changes."
                try:
                    client.messages.create(body=msg, from_=twilio_number, to=f['phone'])
                    logger.info(f"SMS sent to {f['name']} at {f['phone']} (Distance: {distance:.2f}m) — Zone: {f['zone']}")
                except Exception as e:
                    logger.error(f"Failed to send SMS to {f['name']} ({f['phone']}): {e}")
            else:
                logger.info(f"Skipped {f['name']} — too far ({distance:.2f}m)")

# Run the function
send_alert_to_capitol_hotel()

# Capitol Hotel location (change this if needed)
capitol_hotel_location = (17.6868, 83.2185)

# Friends' updated location to Capitol Hotel
friends = [
    {"name": "Praneetha", "phone": "‪+918074474677‬", "loc": capitol_hotel_location, "zone": "Green Zone"},  # Set to Capitol Hotel
    {"name": "hema", "phone": "‪+918328611819‬", "loc": capitol_hotel_location, "zone": "Green Zone"},    # Set to Capitol Hotel
    ]

def send_alert_to_capitol_hotel():
    print("🔔 Sending Alerts to Capitol Hotel contacts...")
    for f in friends:
        if f["loc"] == capitol_hotel_location:  # Only send messages to Capitol Hotel location
            distance = geodesic(capitol_hotel_location, f["loc"]).meters
            if distance <= 3000:  # Only send messages to those within 3 km of Capitol Hotel
                msg = f"Hi {f['name']}! 🌱 Your area is under a GREEN ZONE Alert. The dam storage levels are safe, but stay alert and prepared for any changes."
                try:
                    client.messages.create(body=msg, from_=twilio_number, to=f['phone'])
                    print(f"✅ SMS sent to {f['name']} at {f['phone']} (Distance: {distance:.2f}m) — Zone: {f['zone']}")
                except Exception as e:
                    print(f"❌ Failed to send SMS to {f['name']} ({f['phone']}): {e}")
            else:
                print(f"ℹ Skipped {f['name']} — too far ({distance:.2f}m)")

# Run the function
send_alert_to_capitol_hotel()
