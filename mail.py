import smtplib
from datetime import datetime
import pytz
import json
import os


# Ensure that time is in SG timezone
def utc_to_time(naive, timezone="Singapore"):
  return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))

def send_email(isSuccessful = True):
  email = os.environ.get("EMAIL")

  # set up the SMTP server
  now = utc_to_time(datetime.utcnow())
  s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
  s.starttls()
  s.login("auto-temp@outlook.com", "lmaoboi123")

  FROM = "auto-temp@outlook.com"
  TO = email
  
  if isSuccessful:
    SUBJECT = "TTS Posted"
    TEXT = f'''Your temperature was successfully updated on {now.strftime("%B %d, %Y")} at {now.strftime("%H:%M:%S")}. Stay safe from COVID-19! :)
Note: Do record your temperature manually and stop the script IF YOU'RE NOT FEELING WELL
    '''
  else:
    SUBJECT = "TTS FAILED"
    TEXT = f'''Your temperature failed to update on {now.strftime("%B %d, %Y")} at {now.strftime("%H:%M:%S")}.
Please record your temperature manually and report the bug to the github contributors if you know them. Thanks!'''

  message = "Subject: {}\n\n{}".format(SUBJECT, TEXT)
  print("Sending mail")
  s.sendmail(FROM, TO, message)
  s.quit()

  if __name__ == "__main__":
    send_email()