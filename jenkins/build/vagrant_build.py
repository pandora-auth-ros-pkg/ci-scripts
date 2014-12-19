#!/usr/bin/env python

from __future__ import print_function
from __future__ import with_statement
import sys
import os
import vagrant
import subprocess
import template_files
import argparse
from fabric.api import local, env, run, open_shell, task, execute
from fabric.context_managers import cd, lcd, quiet, show, hide, path

def vagrant_up(vm):
  try:
    print("Starting up vagrant...")
    vm.up()
  except subprocess.CalledProcessError as e:
    print('Something went wrong while "vagrant up":', e)
    vagrant_destroy(vm)
    sys.exit(1)

def vagrant_destroy(vm):
  try:
    print('\nDestroying  vagrant...')
    vm.destroy()
  except subprocess.CalledProcessError as e:
    print('Sometring went wrong while "vagrant destroy:"', e)
    sys.exit(1) # maybe finish cleanly?

def configure(vm, args):
  try:
    global env
    env.hosts = [vm.user_hostname_port()]
    env.key_filename = vm.keyfile()
    env.disable_known_hosts = True # useful for when the vagrant box ip changes.
    env.shell = '/bin/bash -l -i -c'
    env.colorize_errors = True
    env.warn_only = True
    env.output_prefix = False
    env.forward_agent = args.no_forward_agent
  except:
    vagrant_destroy(vm)
    raise

@task
def run_build():
  with cd('/vagrant'), show('output'), hide('running', 'warnings'):
    # this is needed in order to add github to known_hosts; find a more elegant way
    #run('ssh -T git@github.com -oStrictHostKeyChecking=no')
    run('ssh-keyscan -H github.com >> ~/.ssh/known_hosts')
    result = run('./run.bash', pty=True)

  return result.return_code


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="""Setups a vagrant instance and starts executing
                              commands in it, based on a .jenkins.yml file located in the root directory.""")
  parser.add_argument('root', help='The root directory in which vagrant should deploy.')
  parser.add_argument('repo_root', help='The root directory of the repo that we are testing. \
                                              A .jenkins.yml file should be found there.')
  parser.add_argument('--image', help='The os image that vagrant should use. \
                                        Default value is "ubuntu/precise64".', default='ubuntu/precise64')
  parser.add_argument('--cpus', help='Number of cpu cores for vagrant to use. \
                                                              Default value is 2.', default='2')
  parser.add_argument('--memory', help='Amount of memory in MB that vagrant should use. \
                                                              Default value is 2048.', default='2048')
  parser.add_argument('--no-forward-agent', help='Disable forward agent when running fabric.', action='store_false')
  args = parser.parse_args()

  # test if '.jenkins.yml' file exists
  jenkins_file = os.path.join(os.path.abspath(args.repo_root), '.jenkins.yml')

  if not os.path.isfile(jenkins_file):
    print('This repo/branch does not have a ".jenkins.yml" file, abording current build...')
    sys.exit(2)

  # generate Vagrant file at root dir
  template_files.prepare_vagrant(os.path.join(os.path.abspath(args.root), 'Vagrantfile'),
                                                      args.image, args.cpus, args.memory)

  # generate run.bash file at root dir
  template_files.prepare_bash(jenkins_file, os.path.join(os.path.abspath(args.root), 'run.bash'))

  # create up a vagrant vm based on the above Vagrantfile
  #vm = vagrant.Vagrant(os.path.abspath(args.root), quiet_stdout=False, quiet_stderr=False)
  vm = vagrant.Vagrant(os.path.abspath(args.root))

  # starting up the vm
  vagrant_up(vm)

  # configure fabric
  configure(vm, args)

  # run the run.bash in the vm
  status = execute(run_build)

  # cleanup
  vagrant_destroy(vm)

  sys.exit(status)

