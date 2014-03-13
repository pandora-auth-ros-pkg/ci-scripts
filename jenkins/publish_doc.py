#!/usr/bin/env python

import os
import commands
import yaml

def publish_doc(packages, output_dir):
  repo_name = os.getenv('REPO_NAME')
  repos_file = os.getenv('REPOS_FILE')
  public_dir = os.getenv('PUBLIC_DIR')
  
  repo_contents = {}
  repo_contents[repo_name] = packages
  
  if not os.path.isfile(repos_file):
    # copying new docs
    for package in packages:
      cmd = 'rsync -a ' + os.path.join(output_dir, package) + ' ' + public_dir
      print '+', cmd
      os.system(cmd)
    
    doc = open(repos_file, 'w')
    doc.write(yaml.dump(repo_contents))
    doc.close()
  
  else:
    doc = open(repos_file, 'r')
    repos = yaml.safe_load(doc)
    doc.close()
    
    if repo_name in repos:
      # deleting old docs
      for package in repos[repo_name]:
        cmd = 'rm -rf ' + os.path.join(public_dir, package)
        print '+', cmd
        os.system(cmd)
        
    # copying new docs
    for package in packages:
      cmd = 'rsync -a ' + os.path.join(output_dir, package) + ' ' + public_dir
      print '+', cmd
      os.system(cmd)
    
    repos[repo_name] = packages
    doc = open(repos_file, 'w')
    doc.write(yaml.dump(repos))
