import logging
import azure.functions as func
import qatarsale as qs
import extract_details as ext

app = func.FunctionApp()
car_listings = ext.get_car_listings(1)
@app.schedule(schedule="0/60 * * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
#@app.queue_output(arg_name="msg", queue_name="outqueue", connection="AzureWebJobsStorage")
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    car_listings = qs.main(car_listings)
    logging.info('Python timer trigger function executed.')