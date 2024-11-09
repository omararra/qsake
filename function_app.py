import logging
import azure.functions as func
import qatarsale as qs
import extract_details as ext
import time

app = func.FunctionApp()
car_listings = ext.get_car_listings(1)

with open("cars.txt", "w") as f:
    for car in car_listings:
        f.write(f"{car}\n")
@app.schedule(schedule="*/30 * * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
#@app.queue_output(arg_name="msg", queue_name="outqueue", connection="AzureWebJobsStorage")
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info("Fetching current car listings...")
    car_listings = ext.get_car_listings(1)
    # def convert_type(value): 
    #     try: 
    #         return eval(value) 
    #     except: 
    #         return value 
    previous = []
    with open("cars.txt", "r") as file: 
        for line in file:
            previous.append(eval(line.strip()))
    if car_listings == previous:
        logging.info("No new cars")
    else:
        current = qs.main(car_listings, previous)
        for car in current:
            with open("cars.txt", "w") as f:
                f.write(f"{car}\n")
    logging.info("Exiting main function")
    logging.info('Python timer trigger function executed.')