import imaplib
import email

def connect_and_check_imap(server, user, password, port):

  emails = []
  
  imap = imaplib.IMAP4_SSL(server, str(port))
  retcode, state = imap.login(user, password)

  if retcode == 'OK' and state[0] == 'Logged in.':
    retcode, total_mails = imap.select()
    if retcode == 'OK':
      retcode, messages = imap.search(None, 'UnSeen')
  
      if messages[0] != '':
        for num in messages[0].split():
  
          typ, data = imap.fetch(num, '(RFC822)')
          msg = email.message_from_string(data[0][1])
  
          if msg['From'] == 'Travis CI <notifications@travis-ci.org>':
            emails.append(msg)
  
  imap.close()

  return emails
  
