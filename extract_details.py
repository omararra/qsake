import requests
from bs4 import BeautifulSoup
import re
from twilio.rest import Client
def get_car_listings(page):
    print(f"Requesting page {page} of car listings")
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

        print(f"Found {len(car_listings)} car listings on page {page}")
        return car_listings
    print(f"No car listings found on page {page}")
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
