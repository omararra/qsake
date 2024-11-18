import requests
from twilio.rest import Client

def send_message(car_details):
    print("Sending Discord message...")
    webhook_url = "https://discord.com/api/webhooks/1304125279865798756/M1fm8esj8j0MQa5685-D_Q7eynkflmq6o9MAWoZklXFoiezQloBuZt-sDnC7LURJffId"
    data = {
        "content": (
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
            f"Link: <{car_details[9]}>\n"
            f"Image: {car_details[10]}"
        )
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Discord message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
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
        from_='whatsapp:+447311729387',
        to='whatsapp:+97455340079',
    )
    print("Whatsapp message sent:", message.sid)
def main(current, previous):
    new_listings = [car for car in current if car not in previous]
    print(f"New listings: {len(new_listings)}\n")
    
    if new_listings:
        for car in new_listings:
            if car not in previous:
                print(f"Sending message for car: {car[0]} {car[1]} {car[2]}")
                send_message(car)
    
    print("Returning current listings")
    return current
if __name__ == "__main__":
    main()