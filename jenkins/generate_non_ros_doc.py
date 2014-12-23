#!/usr/bin/env python

import sys
from rosdoc_lite import doxygenator
import yaml
import os


class PackageInfo(object):

    __slots__ = ['license', 'maintainer', 'author', 'description', 'status', 'brief', 'url', 'is_catkin', 'exports', 'depends', 'bugtracker', 'repo_url']

    def __init__(self, conf_file):
        with open(conf_file, 'r') as doc:
            confs = yaml.safe_load(doc)

        self.license = confs['license']
        self.maintainer = confs['maintainers']
        self.author = confs['authors']
        self.description = confs['description']
        self.url = confs['url']
        self.bugtracker = confs['bugtracker']
        self.repo_url = confs['repo_url']

        self.status = None
        self.brief = None
        self.is_catkin = None
        self.exports = None
        self.depends = None


def generate_doxygen(path, output_dir):
    # default config, needs in order to use rosdoc_lite
    build_params = {'builder': 'doxygen', 'output_dir': '.'}

    path = os.path.realpath(path)
    output_dir = os.path.join(output_dir, 'html')

    package = os.path.basename(path)

    conf_file = os.path.join(path, 'manifest.yaml')
    manifest = PackageInfo(conf_file)

    doxygenator.generate_doxygen(path, package, manifest, build_params, output_dir, False)


if __name__ == '__main__':
    generate_non_ros_doc(sys.argv[1], sys.argv[2])
