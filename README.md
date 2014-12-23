ci-scripts
==========

scripts used by Jenkins

These scripts are meant to run on a Jenkins master or on a Jenkins slave.
Generally, only scripts that reside in the folder `vagrant_build` should run on a Jenkins
slave. All other scripts should run on the master.

In order to deploy the scripts, certain dependencies have to be met. See the file
`DEPEND` for more information.
