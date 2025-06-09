from datetime import datetime, time

from src.send_email import send_email

if __name__ == "__main__":
    today = datetime.combine(datetime.today().date(), time(7, 0))
    # today = datetime.combine(datetime.today().date(), time(16, 0))
    send_email(today)
