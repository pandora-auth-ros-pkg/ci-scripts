#!/usr/bin/env python

import yaml
import re
import imap_client
import smtp_client
import github_api
import email
import time
import os

default_recipients = ['Chris Zalidis <zalidis@gmail.com>']

def get_credentials():
  credentials_file = os.getenv('CREDENTIALS_FILE')
  if not credentials_file:
    credentials_file = 'credentials.yml'
  doc = open(credentials_file, 'r')
  credentials = yaml.safe_load(doc)
  doc.close()

  return (credentials['server_name'],
          credentials['user_name'],
          credentials['password'],
          credentials['imap_port'],
          credentials['smtp_port'])

def get_commit_from_mail(mail):

  return re.findall(r'Commit: ([0-9a-z]+)', mail.as_string())[0]

def check_and_forward_mail(server, user, password, imap_port, smtp_port):

  new_emails = imap_client.connect_and_check_imap(server, user, password, imap_port)

  for mail in new_emails:
    commit_sha = get_commit_from_mail(mail)
    recipients = []
    commit_author = github_api.get_commit_author('pandora-auth-ros-pkg', 'pandora_ros_pkgs', commit_sha)
    recipients.append(commit_author)

    print 'New mail, Subject:', mail['Subject'] 

    recipients += default_recipients
    smtp_client.send_mail(server, user, password, smtp_port, mail, mail['From'], set(recipients))

if __name__ == '__main__':
  server, user, password, imap_port, smtp_port = get_credentials()
  check_and_forward_mail(server, user, password, imap_port, smtp_port)
