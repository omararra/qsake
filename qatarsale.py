import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_message(car_details):
    print("Sending Discord message...")
    webhook_url = "https://discord.com/api/webhooks/1304917955603071066/X-m3t_bmut_ZMr7eh5_9NCbTlPXid2sWIevcBfiT0x014B6NLKXRpV7fmxkoOzhjy4zT"
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
    print("Sending Email message...")
    message = Mail(
        from_email='info@oryxdev.tech',
        to_emails='smokadem@gmail.com',
        subject='New Listing',
        html_content=(
            f"New car listing:<br>"
            f"<strong>Make:</strong> {car_details[0]}<br>"
            f"<strong>Model:</strong> {car_details[1]}<br>"
            f"<strong>Submodel:</strong> {car_details[2]}<br>"
            f"<strong>Price:</strong> {car_details[3]} QAR<br>"
            f"<strong>Type:</strong> {car_details[4]}<br>"
            f"<strong>Year:</strong> {car_details[5]}<br>"
            f"<strong>Gear Type:</strong> {car_details[6]}<br>"
            f"<strong>Cylinders:</strong> {car_details[7]}<br>"
            f"<strong>Mileage:</strong> {car_details[8]}<br>"
            f"<strong>Link:</strong> <a href='{car_details[9]}'>Click Here</a><br>"
        ))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
    except Exception as e:
        print(e.message)
    # print("Sending WhatsApp message...")
    # account_sid = 'ACcc19f7f4b5e9972e26f19afc773a076a'
    # auth_token = '9c901fee2bb955dd749acc740f2466d2'
    # client = Client(account_sid, auth_token)
    
    # message = client.messages.create(
    #     body=(
    #         f"New car listing:\n"
    #         f"Make: {car_details[0]}\n"
    #         f"Model: {car_details[1]}\n"
    #         f"Submodel: {car_details[2]}\n"
    #         f"Price: {car_details[3]} QAR\n"
    #         f"Type: {car_details[4]}\n"
    #         f"Year: {car_details[5]}\n"
    #         f"Gear Type: {car_details[6]}\n"
    #         f"Cylinders: {car_details[7]}\n"
    #         f"Mileage: {car_details[8]}\n"
    #         f"Link: {car_details[9]}"
    #     ),
    #     from_='whatsapp:+97477086807',
    #     to='whatsapp:+97455741660',
    # )
    # print("Whatsapp message sent:", message.sid)
def main(current, previous):
    new_listings = [car for car in current if car not in previous]
    print(f"New listings: {len(new_listings)}\n")
    
    if new_listings:
        for car in new_listings:
            if car not in previous:
                print(f"Sending message for car: {car}")
                send_message(car)
    
    print("Returning current listings")
    return current
if __name__ == "__main__":
    main()