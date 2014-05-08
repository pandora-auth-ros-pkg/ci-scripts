import smtplib

def send_mail(server, user, password, mail_message, sender, recipients):
  
  mail_message.replace_header('To', ', '.join(recipients))

  session = smtplib.SMTP(server)
  session.login(user, password)
  session.sendmail(sender, recipients, mail_message.as_string())
  session.quit()
