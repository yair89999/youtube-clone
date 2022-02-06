import os,smtplib



sending_email = os.environ.get("WEBSITES_EMAIL")
sending_email_password = os.environ.get("WEBSITES_EMAIL_PASSWORD")

def send(to,email):
    # sending email function
    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sending_email,sending_email_password)
        
        subject = "Reset password in instagram clone"
        body = email

        msg = f"Subject: {subject}\n\n{body}"
        
        smtp.sendmail(sending_email, to,msg)