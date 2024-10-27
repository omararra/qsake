import logging
import azure.functions as func
import qatarsale as qs
import extract_details as ext
import time

app = func.FunctionApp()
@app.schedule(schedule="* * * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
#@app.queue_output(arg_name="msg", queue_name="outqueue", connection="AzureWebJobsStorage")
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    print("Fetching current car listings...")
    car_listings = ext.get_car_listings(1)
    print("Returning current listings")
    print("Sleeping for 10 seconds")
    seconds = 10
    while seconds > 0:
        print(f"Time left: {seconds} seconds")
        time.sleep(1)  # Wait for 1 second
        seconds -= 1
    print("Calling main function...")
    qs.main(car_listings)
    print("Exiting main function")
    logging.info('Python timer trigger function executed.')