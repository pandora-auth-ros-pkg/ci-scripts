#!/usr/bin/env python

import yaml
import os
import argparse

parser = argparse.ArgumentParser(description='Create a repos.yml file mapping each package to corresponding repo')
parser.add_argument('root_of_pkgs', help='The root directory of packages')
args = parser.parse_args()

package_dirs = {}

for root, dirs, files in os.walk(args.root_of_pkgs):
  if '.git' in dirs:
    package_dirs[root] = []

for repo in package_dirs:
  for root, dirs, files in os.walk(repo):
    if 'package.xml' in files:
      package_dirs[repo].append(os.path.basename(root))

for repo in package_dirs:
  package_dirs[os.path.basename(repo)] = package_dirs.pop(repo)

print package_dirs

doc = open('repos.yml', 'w')
doc.write(yaml.dump(package_dirs))
doc.close()
