from datetime import datetime
# from datetime import time

from src.send_email import send_email

if __name__ == "__main__":
    # today_morning = datetime.combine(datetime.today().date(), time(7, 0))
    # today_evening = datetime.combine(datetime.today().date(), time(16, 0))
    today = datetime.today()
    send_email(today)
