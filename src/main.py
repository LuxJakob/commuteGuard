from datetime import datetime

from src.send_email import send_email

if __name__ == "__main__":
    today = datetime.today()
    send_email(today)
