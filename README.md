postgres-kill
=============

Python script to nuke PostgreSQL DB (non-cluster i.e.)

#### Table of contents

1. [Overview] (#overview)
2. [Code Description - what the Python code essentially does] (#code description)
3. [Prerequisites] (#prerequisites)
4. [Limitations - OS compatibility] (#limitations)
5. [Future enhancements - additional functionality that will be added] (#enhancements)


## Overview

The Python script will offer the user varied options to nuke a non-cluster PostgreSQL DB. This program was writted by an aimless guy (yours truly) and is intended for fun. The script has been designed and tested on Ubuntu (10.04 and abovd). Please note that the script when executed will render PostgreSQL DB unrecoverable. Caution is adviced.

## Code Description

This script will go about nuking a standalone PostgreSQL DB

## Prerequisites

* AWS/Rackspace/DigitalOcean node running Ubuntu. (I am currently running Ubunty Trusty: 14.04 LTS)

* Install configuration management tools of choice (masterless mode is easier). I chose Puppet. Send me an email if you you want instructions to automatically spin up nodes/EC2 instances and have Puppet install and configure PostgreSQL DB

* Next, install Python ( I am using Pything 3.4) and psycopg2 which is a PostgreSQL adapter. For instructions on how to install and configure Python and psycopg2 please send me an email.

* Install stressapptest tool via apt-get

* Programatically create test DB instance along with a table and create some garbage entries.

* Configure the security groups (firewall) on the cloud management interface (AWS/RackSpace/DigitalOcean) so that PostgreSQL port 5432 is accessible

## Limitations

The Python script has been only tested on Ubuntu (10.04 +). I have also discovered a race condition when trying to max out the userspace memory on the OS and currently working on a fix to address this.

## Enhancements

Future enhancements will include:

* Support for other flavors of *nix
* Python unit test cases
* Optimizing the program with multiprocessing.

Please report bugs to satish.muthaliATgmail.com
