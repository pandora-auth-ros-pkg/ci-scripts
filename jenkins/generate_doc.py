#!/usr/bin/env python
'''
script for generating documentation automatically
using rosdoc_lite, given a collection of ros  or non-ros packages.

In order to create documentation for non-ros packages a manifest.yaml
file needs to be present.

USAGE: ./generate_doc.py <path_to_root_of_pkgs> <output dir>

Author: Chris Zalidis
'''
import os
import sys
import commands
import argparse
from publish_doc import publish_doc
import generate_non_ros_doc

parser = argparse.ArgumentParser(description='Generate documentation')
parser.add_argument('root_of_pkgs', help='The root directory of packages')
parser.add_argument('output_dir', help='The directory to put html files')
args = parser.parse_args()

rosdoc = 'rosdoc_lite '

package_dirs = {}
non_package_dirs = {}

for root, dirs, files in os.walk(args.root_of_pkgs):
    if 'package.xml' in files:
        package_dirs[os.path.basename(root)] = root

    # for non ros packages try to find a manifest.yaml file
    if 'manifest.yaml' in files:
        non_package_dirs[os.path.basename(root)] = root

if not os.path.isdir(args.output_dir):
    os.mkdir(args.output_dir)

for package in package_dirs:
    out_path = os.path.join(args.output_dir, package)
    cmd = rosdoc + '-o ' + out_path + ' ' + package_dirs[package]
    print '+', cmd
    (status, output) = commands.getstatusoutput(cmd)
    if status:
        sys.stderr.write(output)
        sys.exit(1)
    print output

    # make index-msg.html default page for packages containing msgs
    if 'communications' in package  or 'msgs' in package:
        file = open(os.path.join(out_path, 'html/.htaccess'), 'w')
        file.write('DirectoryIndex index-msg.html\n')
        file.close()

# we are documenting non ros packages
for package in non_package_dirs:
    out_path = os.path.join(args.output_dir, package)
    generate_non_ros_doc.generate_doxygen(non_package_dirs[package], out_path)

publish_doc(package_dirs.keys() + non_package_dirs.keys(), args.output_dir)
