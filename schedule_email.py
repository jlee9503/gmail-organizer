import schedule
import time

def sendScheduled_email():
    print("I am a scheduled job")
    return schedule.CancelJob
    
schedule.every(5).seconds.do(sendScheduled_email)
#schedule.every().day.at('22:30').do(sendScheduled_email)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
