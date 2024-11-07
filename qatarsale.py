from twilio.rest import Client
import extract_details as ext

# Function to send WhatsApp message with car details
def send_whatsapp_message(car_details):
    print("Sending WhatsApp message...")
    account_sid = 'ACcc19f7f4b5e9972e26f19afc773a076a'
    auth_token = '9c901fee2bb955dd749acc740f2466d2'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=(
            f"New car listing:\n"
            f"Make: {car_details[0]}\n"
            f"Model: {car_details[1]}\n"
            f"Submodel: {car_details[2]}\n"
            f"Price: {car_details[3]} QAR\n"
            f"Type: {car_details[4]}\n"
            f"Year: {car_details[5]}\n"
            f"Gear Type: {car_details[6]}\n"
            f"Cylinders: {car_details[7]}\n"
            f"Mileage: {car_details[8]}\n"
            f"Link: {car_details[9]}"
        ),
        from_='whatsapp:+97477086807',
        to='whatsapp:+97455340079',
    )
    print("Message sent:", message.sid)
def main(previous):
    current = ext.get_car_listings(1)
    print("Fetching current car listings...")
    
    new_listings = [car for car in current if car not in previous]
    print(f"New listings: {len(new_listings)}\n")
    
    if new_listings:
        for car in new_listings:
            if car not in previous:
                print(f"Sending WhatsApp message for car: {car}")
                send_whatsapp_message(car)
    
    print("Returning current listings")
    return current
if __name__ == "__main__":
    main()