#!/usr/bin/env python

import yaml
import catkin_pkg.packages
import argparse
import os
import sys
from subprocess import call, check_call

parser = argparse.ArgumentParser(description='Checks if a package has been added or deleted and updates the repos.yml file')
parser.add_argument('root_of_pkgs', help='Root directory of packages')
parser.add_argument('repo_name', help='Name of repo')
parser.add_argument('repos_file', help='Path to repos.yml')
args = parser.parse_args()

doc = open(args.repos_file, 'r')
repos = yaml.safe_load(doc)
doc.close()

pkgs = catkin_pkg.packages.find_packages(args.root_of_pkgs)

packages = [pkg.name for pkg in pkgs.values()]

if set(repos[args.repo_name]) == set(packages):
  print 'Nothing changed'

else:
  print 'Updating packages...'
  repos[args.repo_name] = packages
  doc = open(args.repos_file, 'w')
  doc.write(yaml.dump(repos))
  doc.close()

  # Commit changes
  scripts_path = os.getenv('JENKINS_SCRIPTS')
  cmd = 'cd ' + scripts_path
  print '+', cmd
  check_call(cmd, shell=True)
  cmd = 'git add -u'
  print '+', cmd
  check_call(cmd, shell=True)
  cmd = "git commit -m 'Update repos.yml'"
  print '+', cmd
  check_call(cmd, shell=True)
  cmd = 'git push origin master'
  print '+', cmd
  check_call(cmd, shell=True)

sys.exit(0)
