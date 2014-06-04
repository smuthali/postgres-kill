#!/usr/bin/python
from socket import p
import psycopg2
import psycopg2.extras
import sys
import os
import subprocess
from subprocess import call
import re
import errno
import shutil
import commands
import getopt
import argparse
import time

__author__ = 'smuthali'

# Define global assignments here (Note: Python does not have a concept of variables)
dbStatus = "None"
fsfull = 100

# core logic functions here

# function 1: check DB connectivity status
def checkdbconnect():
    try:
        conn = psycopg2.connect("host='localhost' database='dbtest' user='postgres'")
        print "Connected to PostgreSQL DB\n"
        cur = conn.cursor()
        assert isinstance(cur, object)
        service_status = commands.getoutput('ps -A')
        if 'postgres' in service_status:
            print(" Postgres running ")
            dbStatus = "Online"
            return dbStatus
        else:
            dbStatus = "Offline"
            print (" Postgres is offline! ")
            return dbStatus

    # Catch the exception if DB connection fails
    except psycopg2.DatabaseError as e:
        print("Unable to connect to the PostgreSQL DB, check if the postgresql service is running")
        print 'Error %s' % e
        dbStatus = "Offline"
        return dbStatus


# function 2: check current disk occupancy
def checkfs():
    # assign disk occupancy to 100
    fsfull = 100
    # first check to make sure filesystem is not full
    df_output_lines = [s.split() for s in os.popen("df -h").read().splitlines()]
    df_output_row = df_output_lines[1]
    df_output_row = df_output_row[4]
    df_output_row = df_output_row.translate(None, '%')
    assert isinstance(df_output_row, object)
    print df_output_row
    return df_output_row


# function 3: check available freespace
def checkavail():
    df_output = [s.split() for s in os.popen("df -h").read().splitlines()]
    df_output_avail = df_output[1]
    df_output_avail = df_output_avail[3]
    assert isinstance(df_output_avail, object)
    return df_output_avail


# function 4: check status of postgres service
def checkPostgres():
    # Function to check the status of PostgreSQL DB
    service_status = commands.getoutput('ps -A|grep postgres')
    if 'postgres' in service_status:
        assert isinstance(service_status, object)
        print ("Postgres running status:\n%s" % service_status)
        print (" Postgres still running!")
        return service_status
    else:
        print (" Postgres not running or has crashed!")
        assert isinstance(service_status, object)
        return service_status


# function 5: restart Postgres
def restartPostgres():
    # Function to restart Postgres
    # This function is more of a sanity check to ensure Postgres has not truly crashed
    # So the function simply restarts postgres to confirm postgres is 'truly' running
    try:
        command = ['service', 'postgresql', 'restart'];
        retcode = subprocess.check_call(command, shell=False)
        print "The PostgreSQL retrun code from its restart is: %s" % retcode
        if retcode == 1:
            print "PostgreSQL failed to start, problem with Postgres - please investigate"
            return retcode
        else:
            print "PostgreSQL started up successfully"
            return retcode
    except subprocess.CalledProcessError as e:
        print ("PostgreSQL restart failed")
        raise RuntimeError("PostgreSQL restart failed")
        return retcode


# function 6: Max filesystem out
def fillhdd():
    global e
    print (" Maxing the filesystem out, please wait:")
    fileop = subprocess.Popen("dd if=/dev/zero of=zeros bs=1M", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    print 'fileop subprocess = ', fileop.pid
    # write garbage to fill up the fs
    try:
        fsstatus = checkavail()
        print "Current filesystem availability is -> %s" % fsstatus
        print "\n"
        if fsstatus == "0":
            # give a few seconds so that the parent process can reap it's child
            time.sleep(3)
            print "Filesystem full, looks like postgres crashed, but will confirm it - break! break! break!"
            break
    except IOError as e:
        # Note that this function will be returning nothing as the exception will be invoked once the fs is maxed out
        ERRCODE = errno.errorcode[errno.ENOSPC]
        print "ERRCODE -> %s" % ERRCODE
        print e.errno
        print e
        return ERRCODE

    # this is where we confirm if Postgres has truly crashed
    postgresStatus = restartPostgres()
    if postgresStatus == 0:
        nukeStatus = "Negative"
        print "PostgreSQL started up successfully"
        return nukeStatus
    else:
        nukeStatus = "Positive"
        print "PostgreSQL has crashed"
        return nukeStatus


# function 7: delete postgres data dir
def nukePGdir():
    dirpath = "/var/lib/postgresql/%s/main/data"
    try:
        datadir = shutil.rmtree(dirpath % pgversion)
        # check to make sure postgres has crashed indeed
        service_status = commands.getoutput('ps -A|grep postgres')
        if 'postgresql' in service_status:
            print("postgres still running!")
            return service_status
        else:
            print("Postgres crashed/dead!")
            return service_status
    except OSError as e:
        print ( " Oops the directory in question is not present ")
        ERR = "NODIR"
        return ERR


# function 8: delete postges pg_clog dir
def nukePGclog():
    try:
        dirpath = "/var/lib/postgresql/%s/main/pg_clog"
        pg_translog = shutil.rmtree(dirpath % pgversion)
        service_status = commands.getoutput('ps -A|grep postgres')
        if 'postgres' in service_status:
            print("Postgres still running!")
            return service_status
        else:
            print("Postgres crashed/dead!")
            return service_status
    except OSError as e:
        ERR = "NODIR"
        print ("Oops the directory in question is not present")
        return ERR


# function 9: max out the userspace memory
def memMax():
    print "task: Consume the userspace memory on the OS"
    print "To run this task the stressapptest tool is required (https://code.google.com/stressapptest)"
    print "The program will check to see if stressapptest is installed, if not then the program will exit and prompt the user to install the tool"
    print "Note: currently tested only on Ubuntu 10.04, 12.04 and 13.10"
    print "/n"
    print "Checking to see if stressapptest is installed"
    devnull = open(os.devnull, "w")
    checkPkg = subprocess.call(["dpkg", "-s", "stressapptest"], stdout=devnull,stderr=subprocess.STDOUT)
    devnull.close()
    if checkPkg == 0:
        print "stressapptest is installed on the system, continuing with the task"
        # run appstresstest for 20 seconds and restart postgres to ensure postgres has crashed.
        # first, calculate total available (userspace) memory i.e. RAM + Swap
        freecalc = [s.split() for s in os.popen("free -ht").read().splitlines()]
        freecalc_total = freecalc[4]
        freecalc_total = freecalc_total[3]
        freecalc_total = freecalc_total.translate(None, 'M')
        print "The total available userspace memory including swap is: %s" % freecalc_total
        # now feed the freecalc_total to stressapptest tool
        assert isinstance(freecalc_total, object)
        total_mem = "%s" % freecalc_total
        command = "stressapptest -M %s -s 20" % total_mem
        try:
            p = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p == 0:
                print "stressapptest execution successful"
                return p
            else:
                print "stressapptest execution failed"
                return p
        except:
            raise RuntimeError("stressapptest execution failed")
            return p

    else:
        print "stressapptest not installed. Please run # apt-get install stressapptest to install the tool"
        raise RuntimeError("stressapptest not installed. Please run # apt-get install stressapptest to install the tool")
        return checkPkg


# function 10: check status of PostgreSQL DB service
def checkPostgres():
    # Function to check the status of PostgreSQL DB
    service_status = commands.getoutput('ps -A|grep postgres')
    if 'postgres' in service_status:
        assert isinstance(service_status, object)
        print ("Postgres running status:\n%s" % service_status)
        print (" Postgres still running!")
        return service_status
    else:
        print (" Postgres not running or has crashed!")
        return service_status


# function 11: restart PostgreSQL DB
def restartPostgres():
    # Function to restart Postgres
    # This function is more of a sanity check to ensure Postgres has not truly crashed
    # So the function simply restarts postgres to confirm postgres is 'truly' running
    try:
        command = ['service', 'postgresql', 'restart'];
        retcode = subprocess.check_call(command, shell=False)
        print "The PostgreSQL retrun code from its restart is: %s" % retcode
        if retcode == 1:
            print "PostgreSQL failed to start, problem with Postgres - please investigate"
            return retcode
        else:
            print "PostgreSQL started up successfully"
            return retcode
    except subprocess.CalledProcessError as e:
        print ("PostgreSQL restart failed")
        raise RuntimeError("PostgreSQL restart failed")
        return retcode

# function 12: select options
def selectopts():
    # obtain the postgresql version and assign its value to pgversion variable
    global pgversion
    pgVer = [s.split() for s in os.popen("psql --version").read().splitlines()]
    print pgVer[0]
    for i, var in enumerate(pgVer[0]):
        if i == len(pgVer[0]) - 1:
            pgversion = var
            pgversion = pgversion.replace(' ','')[:-2]

    print "pgversion value is \n %s" % pgversion

    # delete one of the core postgres directories
    # prompt the user with different options here (pg_clog, data dir etc...)
    # here's the menu
    print ("option1. Nuke the data directory")
    print ("option2. Nuke the master transaction log directory, i.e. pg_clog. Note: this will be an unrecoverable crash!")
    print ("option3. Run another program that will eat up all of the available memory, this will cause postgres to crash")
    print ("option4. Nuke pg_xlog, this will mess up PostgreSQL WAL internals, this will cause postgres to crash" )
    print ("option5. Just pkill the parent postgres pids" )



# function 13: (lucky 13!) - one of the main functions executing core logic
def execute():
    nuke_options = 0
    lim = 5
    lower_lim = 0
    selectopts()
#    nuke_options = 0
    is_valid = 0
    while not is_valid:
        try:
            nuke_options = int ( raw_input("Specify your option [1-5] : ") )
            is_valid=1
            print "nuke_options=%s" % nuke_options
            if nuke_options == 1:
                print("User has chosen option:%s" % nuke_options)
                # invoke postgres pg dir nuke
                print("Invoking logic to nuke the pg directory")
                nukePGdirStatus = nukePGdir()
                if not nukePGdirStatus:
                    print("PostgreSQL DB has crashed - pg directory has been nuked")
                    sys.exit(0)
                else:
                    print("Failed to nuke PostgreSQL DB => most likely a logic problem")
                    return sys.exit(2)

            elif nuke_options == 2:
                print("User has chosen option:%s" % nuke_options)
                # Invoke logic to nuke pg_clog dir
                nukePGclogStatus = nukePGclog()
                if not nukePGclogStatus:
                    print("PostgreSQL DB has crashed - pg_clog has been nuked")
                    sys.exit(0)
                else:
                    print("Failed to nuke PostgreSQL DB => most likely a logic problem")
                    sys.exit(2)

            elif nuke_options == 3:
                print("User has chosen option:%s" % nuke_options)
                # invoke logic to max out memory
                print ("running another program in background that will consume all of available memory on the AWS instance")
                jobs = []
                for f in [memMax, restartPostgres]:
                    print "Starting to process function", f.func_name
                    j = multiprocessing.Process(target=f, name=f.func_name)
                    jobs.append(j)
                    j.start()

                for j in jobs:
                    j.join()
                    print "%s.exitcode = %s" % (j.name, j.exitcode)

                proc_stressexit_code = jobs[0].exitcode
                proc_pgexit_code = jobs[1].exitcode

                if proc_stress_code == 0:
                    print "stressapptest execution successful"
                    # now check if restartPostgres failed - by all means we want this to fail
                    if proc_pgexit_code == 1:
                        print "PostgreSQL DB has crashed because of insufficient shared memory"
                        sys.exit(0)
                    else:
                        print "Shouldn't be hitting this condition, implies => postgres startup successfully"
                        sys.exit(2)
                else:
                    print "Shouldn't be hitting this condition , implies => stressapptest failed to run and we also assume restartPostgres also failed"
                    sys.exit(-2)


            elif nuke_options == 4:
                print"User has chosen option:%s" % nuke_options
                print (" Deleting pg_xlog will mess up the WAL Internals and cause postgres to crap" )
                try:
                    dirpath = "/var/lib/postgresql/%s/main/pg_xlog"
                    delWAL = shutil.rmtree(dirpath % pgversion)
                    service_status = commands.getoutput('ps -A|grep postgres')
                    if 'postgres' in service_status:
                        print("Postgres still running! - which is unexpected => logic problem?")
                        sys.exit(-2)
                    else:
                        print("PostgreSQL DB has crashed!")
                        sys.exit(0)
                except OSError as e:
                    ERR == "NODIR"
                    print("Oops the directory in question is present" )
                    return ERR


            elif nuke_options == 5:
                print("User has chosen option:%s" % nuke_options)
                print ( " Performing a pkill (SIGTERM) on the parent postgres pids" )
                postgreskill = subprocess.Popen(["pgrep", "postgres"], stdout=subprocess.PIPE).communicate()[0]
                # Obtain the Parent PID for postgres
                try:
                    PPID = postgreskill.splitlines()[0] + '\n'
                    print "PPID: -> %s" % PPID
                    if PPID:
                        PID_Kill = os.kill(int(PPID), signal.SIGTERM)
                        ppidRet = "RunningKilled"
                        print "PID_Kill -> %s" % PID_Kill
                        return ppidRet
                        sys.exit(0)
                    else:
                        print "PostgreSQL is stopped, PID value is null. Ensure postgres is running before trying to nuke it"
                        ppidRet = "NotRunning"
                        return ppidRet
                        sys.exit(-2)
                except IndexError:
                    ppidRet = "NotRunning"
                    print (" got null data for PPID, this means Postgres is not running, prerequisite for this task is to have PostgreSQL running")
                    return ppidRet
                    sys.exit(-2)

            else:
                print "Invalid selection, please try again"
                execute()
        except ValueError as e:
            print (" '%s' is not a valid integer." % e.args[0].split(": ")[1])


# Entry point to the program
def main():
    parser = argparse.ArgumentParser(prog='./crashdb.py', usage='%(prog)s [options]')
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("-f", help="Argument fsnuke expected")
    grp.add_argument("-d", help="Argument dirnuke expected")
    args = parser.parse_args()
    if len([x for x in args.f, args.d if x is not None]) > 1:
        raise Exception("Invalid syntax")
    # Ensure correct args are passed
    # As based on the args the appropriate logic will be fired
    if args.f == "fsnuke":
        print ("Passed argument to the script is: -> %s" % args.f)
        print "Invoking logic to fill the filesystem - this will cause PostgreSQL to crash "
        dbConnect = checkdbconnect()
        if dbConnect == "Offline":
            print "Check to make sure PostgreSQL is running"
            sys.exit(2)
        else:
            print "Checking for available diskspace on the filesystem"
            dfCheck = checkfs()
            if eval(dfCheck) == 100:
                print "Filesystem is already full - unable to invoke the required logic."
                print "Clean up the filesystem to make sufficient disk space available\n"
            else:
                print "Invoking logic to nuke the filesystem"
                nukeFS = fillhdd()
                if nukeFS == "Positive":
                    print ("PostgreSQL DB has officially crashed\n")
                else:
                    print ("PostgreSQL DB is still running - which is highly unexpected\n")
                    print ("This means we have a problem in the logic")

    elif args.d == "dirnuke":
        print ("Passed argument to the script is: -> %s" % args.d)
        print "Invoking logic that will provide more options to crash PostgreSQL"
        execute()

    else:
        assert isinstance(parser, object)
        parser.print_help()
        sys.exit(2)

