#!/usr/bin/env python

import os
import re
import time
import paramiko
import yaml
from subprocess import call, check_call, check_output
from random import randint 
from string import Template

server_create = Template('kamaki server create --network=$network --name=$name --flavor-id=$flavor --image-id=$image -p ~/.ssh/id_rsa.pub,/root/.ssh/authorized_keys --wait')
server_info = Template('kamaki server info $id')
server_delete = Template('kamaki server delete $id')

#network_ = '1,192.168.0.73'
#network_ = '4160,192.168.11.133'
network_ = '4159,192.168.4.47'
name_ = 'ci-server-' + str(randint(0, 1000000))
flavor_ = '814'
image_ = 'a6645e73-49ef-4fd2-9293-35329d12730a'

cmd = server_create.substitute(network=network_, name=name_, flavor=flavor_, image=image_)
print '+', cmd
first_out = check_output(cmd, shell=True)

server_id = re.findall(r'id: (\d\d\d\d\d\d)', first_out)[0]
second_out = check_output(server_info.substitute(id=server_id), shell=True)

ip = re.findall(r'ipv6: ([0-9a-fA-F:]+)', second_out)[0]
ssh_port = re.findall(r'port: (\d\d\d\d\d)', second_out)[0]

# wait for server to become ready
time.sleep(40)
#call('ssh root@'+ip+' -o StrictHostKeyChecking=no', shell=True)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(ip, username='root')
ssh.connect('gate.demo.synnefo.org', username='root', port=int(ssh_port))

synnefo_file = os.getenv('SYNNEFO_FILE')
doc = open(synnefo_file, 'r')
yml = yaml.safe_load(doc)
doc.close()

#for cmd in yml['commands']:
  #print '+', cmd
cmds = ';\n'.join(yml['commands'])
print ##
print cmds
print ##

stdin, stdout, stderr = ssh.exec_command(cmds)
for line in stdout.read().splitlines():
  print '...', line
for line in stderr.read().splitlines():
  print '...', line

ssh.close()
