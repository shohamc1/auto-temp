import smtplib
# set up the SMTP server

def send_email():
  s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
  s.starttls()
  s.login("barcelonafcshoham@hotmail.com", "shohamc19960")

  FROM = "barcelonafcshoham@hotmail.com"
  TO = "shhmchk@gmail.com"

  SUBJECT = "TTS Posted"
  TEXT = "Your temperature has been updated. Your sanity has been saved. Stay safe from COVID-19"

  message = "Subject: {}\n\n{}".format(SUBJECT, TEXT)

  s.sendmail(FROM, TO, message)
  s.quit()