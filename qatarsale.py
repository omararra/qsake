import requests
from bs4 import BeautifulSoup
import time
import re
from twilio.rest import Client

# Function to get car listings from the specified page
def get_car_listings(page):
    url = f"https://qatarsale.com/en/products/cars_for_sale?sortBy=AuctionStartTime_desc&page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    allcarsdetails = soup.find("div", class_=re.compile(r"ng-tns-c\d{3}-3 product-list classic ng-star-inserted"))

    # Check if there are car details available
    if allcarsdetails:
        car_listings = []
        details = allcarsdetails.find_all("qs-product-card-v2", class_=re.compile(r"ng-tns-c\d{3}-\d{2} ng-tns-c\d{3}-3 ng-star-inserted"))

        # Extract details for each car listing
        for detail in details:
            car = extract_details(detail)
            car_listings.append(car)

        return car_listings
    return []

# Function to extract details of a car
def extract_details(text):
    car_listing = []

    # Find car visual elements and details
    car_visual = text.find("a", class_="img-loading ng-star-inserted")
    car_link = car_visual.get("href") if car_visual else None
    car_img = car_visual.find("img", class_="prod-img").get("src")
    carinfo = text.find("div", class_="product-definitions")
    carmakemodel = text.find("div", class_="product-details")
    carprice = text.find("div", class_="product-controls").find("p", class_=re.compile(r"p1 ng-tns-c\d{3}-\d{2}")).get_text()
    
    make = carmakemodel.find("p", class_="p3 ng-star-inserted").get_text() if carmakemodel.find("p", class_="p3 ng-star-inserted") else None
    model1 = carmakemodel.find("p", class_="p5 ng-star-inserted").get_text() if carmakemodel.find("p", class_="p5 ng-star-inserted") else None
    submodel = carmakemodel.find("p", class_="p5 sub-header ng-star-inserted").get_text() if carmakemodel.find("p", class_="p5 sub-header ng-star-inserted") else None
    type = carmakemodel.find("p", class_=re.compile(r"ng-tns-c\d{3}-\d{2} p5")).get_text() if carmakemodel.find("p", class_=re.compile(r"ng-tns-c\d{3}-\d{2} p5")) else None
    
    year = carinfo.find("div", style="order:0;").find("span", class_="def-value").get_text() if carinfo.find("div", style="order:0;") else None
    geartype = carinfo.find("div", style="order:1;").find("span", class_="def-value").get_text() if carinfo.find("div", style="order:1;") else None
    cylinders = carinfo.find("div", style="order:2;").find("span", class_="def-value").get_text() if carinfo.find("div", style="order:2;") else None
    mileage = carinfo.find("div", style="order:3;").find("span", class_="def-value").get_text() if carinfo.find("div", style="order:3;") else None
    
    car_listing = [make, model1, submodel, carprice, type, year, geartype, cylinders, mileage, car_link, car_img]
    return car_listing

# Function to send WhatsApp message with car details
def send_whatsapp_message(car_details):
    account_sid = 'ACca76c3474f8f63f7d0cb40df8a3b4082'
    auth_token = '6bd3945c890e12a296409b2f9ad15fa3'
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
        from_='whatsapp:+14155238886',
        to='whatsapp:+97455741660',
    )
    print(message.sid)
def main():
    previous_listings = []
    page = 1
    previous_listings.extend(get_car_listings(page))
    # Save initial listings to a file (currently commented out)
    #with open('qatarsale.txt', 'w') as file:
    #    for car in previous_listings:
    #        file.write(f"{car},\n")
    
    while True:
        time.sleep(10)
        current_listings = []
        current_listings.extend(get_car_listings(page))
        
        # Identify new car listings
        new_listings = [car for car in current_listings if car not in previous_listings]
        if new_listings:
            for car in new_listings:
                print(f"New car listing: {car}")
                send_whatsapp_message(car)
            previous_listings = current_listings

if __name__ == "__main__":
    main()