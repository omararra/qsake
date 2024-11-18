from twilio.rest import Client
car_details = [' Audi ', ' Q3 ', ' 35 TFSI ', ' 85,000 ', None, ' 2020 ', ' Automatic ', ' 4 ', ' 89,000 Km', 'http://qatarsale.com/en/product/audi_q3_35_tfsi_black_suv_automatic_2020-275197', 'https://media-blob.qatarsale.com/275197-productcovers/43c0d30f-2de6-490d-b5b3-baf11e743aed_0_cover.webp']
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
    to='whatsapp:+97455741660',
)
print("Whatsapp message sent:", message.sid)