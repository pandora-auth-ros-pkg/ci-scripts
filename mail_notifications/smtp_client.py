import smtplib

def send_mail(server, user, password, port, mail_message, sender, recipients):
  
  mail_message.replace_header('To', ', '.join(recipients))

  session = smtplib.SMTP(server, int(port))
  session.login(user, password)
  session.sendmail(sender, recipients, mail_message.as_string())
  session.quit()
