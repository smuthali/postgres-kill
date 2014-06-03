postgres-kill
=============

Python script to nuke PostgreSQL DB (non-cluster i.e.)

#### Table of contents

1. [Overview] (#overview)
2. [Code Description - what the Python code essentially does] (#module description)
3. [Prerequisites] (#prerequisites)
    * [Build out a simple PostgreSQL DB] (#Build-postgres)
    * [Create a test database instance and populate some junk] (#create-db-junk)
    * [Install latest version of Python GA] (#install-python)
    * [Install stressapptest tool] (#install-stressapptest)
4. [Usage - how to invoke the Python script] (#usage)
5. [Limitations - OS compatibility] (#limitations)
6. [Future enhancements - additional functionality that will be added] (#enhancements)


## Overview

The Python script will offer the user varied options to nuke a non-cluster PostgreSQL DB. This program was writted by an aimless guy (yours truly) and is intended for fun. The script has been designed and tested on Ubuntu (10.04 and abovd). Please note that the script when executed will render PostgreSQL DB unrecoverable. Caution is adviced.

## Module Description

This script will go about nuking a standalone PostgreSQL DB

## Setup

### Prerequisities

* AWS/Rackspace/DigitalOcean node running Ubuntu. (I am currently running Ubunty Trusty: 14.04 LTS)
* TZ configuration file (/etc/sysconfig/clock)

## Usage
In site.pp it is sufficient to simply add `include '::puppet-tz'` to load, install and configure TimeZone module. Parameters can also be passed to the TimeZone module by specifying the custom timezone. For example:
```puppet
class { '::puppet-tz':
   timezone => 'America/Los_Angeles',
   }
   ```
   
## Limitations

The TimeZone puppet module has been built on and test against Puppet 3.4.2 and has also been tested on Puppet 2.7.
The module has been tested on:

* RedHat Enterprise Linux 6.x
* CentOS 6.x
* Ubuntu 10.04 and 12.04

The TimeZone module has not been tested on Gentoo, SuSe or FreeBSD.

## Enhancements

Future enhancements will include:

* Testing on other flavors of *nix
* More robust RSpec test cases

Please report bugs to satish.muthaliATgmail.com
