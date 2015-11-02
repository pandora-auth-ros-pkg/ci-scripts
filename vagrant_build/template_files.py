#!/usr/bin/env python

import os
import yaml

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

TEMPLATE_BASH_FILENAME = 'run.bash.in'
TEMPLATE_VAGRANT_FILENAME = 'Vagrantfile.in'


def read_file(filename):
    with open(filename, 'r') as f:
        text = f.read()

    return text


def read_yaml(filename):
    with open(filename, 'r') as f:
        yml = yaml.safe_load(f)

    return yml


def write_file(text, filename, exe=False):
    with open(filename, 'w+') as f:
        f.write(text)

    if exe:
        os.chmod(filename, 0775)


def prepare_vagrant(vagrant_filename, image, cpus=1, memory=1024):
    # read vagrantfile template
    vagrantfile = read_file(os.path.join(__location__, TEMPLATE_VAGRANT_FILENAME))

    # replace templated stuff
    vagrantfile = vagrantfile.replace('@OS_TYPE@', image)
    vagrantfile = vagrantfile.replace('@CPUS@', str(cpus))
    vagrantfile = vagrantfile.replace('@MEMORY@', str(memory))

    # write the output file
    write_file(vagrantfile, vagrant_filename)


def prepare_bash(yml_filename, out_filename):
    # read the .jenkins.yml file
    yml = read_yaml(yml_filename)

    for sec in yml.keys():
        # replace single quotes with '\''
        # we need to break single quoting add an
        # escaped quote and quote back in.
        yml[sec] = map(lambda x: x.replace("'", "'\\''"), yml[sec])

        # wrap with single quotes each command,
        # add one quote at the beginning and one at the end.
        yml[sec] = "'{0}'".format("'\n'".join(yml[sec]))

    # read the template file
    bash_script = read_file(os.path.join(__location__, TEMPLATE_BASH_FILENAME))

    # replace commands on the template file
    bash_script = bash_script.replace('@INSTALL@', yml['install'])
    bash_script = bash_script.replace('@SCRIPT@', yml['script'])

    # write to output file
    write_file(bash_script, out_filename, exe=True)

if __name__ == '__main__':
    prepare_bash('.jenkins.yml', 'test.bash')
    prepare_vagrant('Vagrantfile', 'ubuntu/trusty64')
