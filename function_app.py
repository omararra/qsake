import logging
import azure.functions as func
import qatarsale as qs
import extract_details as ext

app = func.FunctionApp()
car_listings = ext.get_car_listings(1)

with open("cars.txt", "w") as f:
    for car in car_listings:
        f.write(f"{car}\n")
@app.schedule(schedule="0 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info("Fetching current car listings...")
    car_listings = ext.get_car_listings(1)
    previous = []
    with open("cars.txt", "r") as file: 
        for line in file:
            previous.append(eval(line.strip()))
    with open("cars.txt", "w") as f:
        f.write("")
    if car_listings == previous:
        logging.info("No new cars")
    else:
        current = qs.main(car_listings, previous)
        for car in current:
            with open("cars.txt", "a") as f:
                f.write(f"{car}\n")
    logging.info("Exiting main function")
    logging.info('Python timer trigger function executed.')
    logging.info("\n\n")