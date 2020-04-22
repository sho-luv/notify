#!/usr/bin/python

# does not use twilio!
# uses mail.smtp.com with creds

import time
import argparse # Parser for command-line options, arguments and sub-commands
import sqlite3 # Check SQLite database for changes in table
import smtplib	# SMTP protocol client
import code # used for debugging with the command "code.interact(local=dict(globals(), **locals()))
import sys # used sys to have clean exits of the program
import smtplib # used to send email so we can do email to text
import os # used to call sendEmail because I didn't want to use python smtplib ....
import subprocess # used to call sendEmail because I didn't want to use python smtplib ....
from termcolor import colored, cprint

# python -m pdb email-to-sms.py # debug program

######################
#
# This progam uses an email smtp to send email to sms messages
# to phone numbers provided on the command line. The sender
# must know the carrier to send the message. However you can
# simply send the message to all carriers in hopes they get it.
#

class Watcher(object):
    running = True
    refresh_delay_secs = 2 

    # Constructor
    def __init__(self, watch_file, watch_sqldb, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.filename = watch_file
        self.sqlfile = watch_sqldb
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    # Look for changes
    def look(self):
        try:
            if self.filename is not None:
                stamp = os.stat(self.filename).st_mtime
                if stamp != self._cached_stamp:
                    self._cached_stamp = stamp
                    # File has changed, so do something...

                    if self.call_func_on_change is None:
                        self.call_func_on_change = "Something"
                        msg = "Notification set to watch file: " + options.file
                        cprint('[+] ', 'green', attrs=['bold'], end='')  # print success
                        cprint(msg,'white') 
                    else:
                        send_email(options.phone, carrier_email, options.m)
            if self.sqlfile is not None:
                try:
                    # note: if there are "Database error: unable to open database file"
                    # errors this is due to the sqlite database being locked by another
                    # process. By default connections will wait 5 seconds befor timeouts
                    # with database locked errors. To avoid this we can increse the
                    # timeout from the default of 5 seconds = 5000 to something like 
                    # 10 seconds or 10000 to avoid thees database locked errors
                    conn = sqlite3.connect(self.sqlfile, timeout=200000)
                    c = conn.cursor()
                    c.execute('SELECT count(*) FROM {tn}'. format(tn=options.table))
                    all_rows = c.fetchall()
                    stamp = all_rows[0][0]

                    if stamp != self._cached_stamp:
                        self._cached_stamp = stamp
                        # File has changed, so do something...

                        if self.call_func_on_change is None:
                            self.call_func_on_change = "Something"
                            msg = "Notification set to watch file: " + options.sqlite
                            cprint('[+] ', 'green', attrs=['bold'], end='')  # print success
                            cprint(msg,'white') 
                        else:
                            send_email(options.phone, carrier_email, options.m)
                except sqlite3.Error as e:
                    print("Database error: %s" % e)
                except Exception as e:
                    print("Exception in _query: %s" % e)
        except AttributeError as e:
            print(e)
            print("Unhandled exception in look function:", sys.exc_info()[0])
            exit()

    # Keep watching in a loop        
    def watch(self):
        while self.running:
            try:
                # Look for changes
                time.sleep(self.refresh_delay_secs)
                self.look()
            except KeyboardInterrupt:
                print('\nDone')
                break
            except FileNotFoundError as e:
                # Action on file not found
                #print(e)
                print(e)
                break
            except:
                print('Watch Unhandled error: %s' % sys.exc_info()[0])


def is_valid_number(phone_number):
    if len(phone_number) != 12:
        return False
    for i in range(12):
        if i in [3,7]:
            if phone_number[i] != '-':
                return False
        elif not phone_number[i].isalnum():
            return False
    return True

def checkvalidNumber(number):
    if len(number) != 10 and number.isdigit():
        return False
    else:
        return True

def send_email(number, carrier_email, message):

    #main
    email = "sendEmail -f %s -t %s%s -u %s "\
            "-s %s:%s -o tls=no -xu %s -xp %s -m %s"\
            % (from_email, number, carrier_email, email_subject, smtp_server, \
            smtp_port, username, password, message)
    try:
        # call to os to run command and save output
        output = subprocess.check_output(email, shell=True, universal_newlines=True) 
    except Exception as e:
        cprint('Email Send Error: ', 'red', end='')  # print out carrier information
        print(e)
        return False

    if 'successfully' in output:
        cprint('[+] ', 'green', attrs=['bold'], end='')  # print success
        cprint(output[0:16], end='')    # print out date and timestamp of message sent
        response = " Message sent to %s on the %s network" % (yellow_phone, color_carrier)
        print(response)
        return True
    else:
        cprint("Sorry unable to send message...", 'red', attrs=['bold'])
        return False
        
if __name__ == "__main__":
    # executes only if run as a script

    banner = """
        888b    888          888    d8b  .d888
        8888b   888          888    Y8P d88P"
        88888b  888          888        888
        888Y88b 888  .d88b.  888888 888 888888 888  888
        888 Y88b888 d88""88b 888    888 888    888  888
        888  Y88888 888  888 888    888 888    888  888
        888   Y8888 Y88..88P Y88b.  888 888    Y88b 888
        888    Y888  "Y88P"   "Y888 888 888     "Y88888
                                                    888
                                               Y8b d88P
                                                "Y88P"
    """

    
    # SMTP settings server and credentials
    #################################################################
    smtp_server = 'mail.smtp.com'	# gmail smtp: smtp.gmail.com								
    smtp_port = '2525'				# gmail port: 587
    from_email = 'notify@computer.com'
    email_subject = 'notify.py'
    username = ''    		# username
    password = 'test' # password 
    #################################################################


    parser = argparse.ArgumentParser(description='This program sends text messages to people using by using email.')
    parser.add_argument('phone', action='store', metavar='phone',help="Phone number to send text message to.\n Phone "
                                                            "number should have no spaces and be of format ##########")
    parser.add_argument('-m', action='store', metavar = '"msg"', help='Text message')
    parser.add_argument('-u', action='store', metavar = 'username', help='SMTP username')
    #group = parser.add_mutually_exclusive_group()
    group = parser.add_argument_group('carrier')
    group.add_argument('-att', action='store_true', help='Send text message to AT&T Wireles')
    group.add_argument('-cricket', action='store_true', help='Send text message to Cricket')
    group.add_argument('-google', action='store_true', help='Send text message to Google')
    group.add_argument('-sprint', action='store_true', help='Send text message to Sprint')
    group.add_argument('-tmobile', action='store_true',  help='Send text message to T-Mobile')
    group.add_argument('-verizon', action='store_true', help='Send text message to Verizon Wireless')
    group.add_argument('-all', action='store_true', help='Send text message to all networks')
    group2 = parser.add_argument_group('Notify options')
    group2.add_argument('-file', action='store', metavar = 'File', help='Send notification if file changes')
    group2.add_argument('-sqlite', action='store', metavar = 'sqlite.db', help='Send notification if table in sqlite.db changes also requires -table option')
    group2.add_argument('-table', action='store', metavar = 'table_name', help='Send notification if table in sqlite.db changes')


    #code.interact(local=dict(globals(), **locals())) # debug

    if len(sys.argv)==1:
        print(banner)
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()

    if not username and options.u is None and not password:
        print( "\nPlease set SMTP settings inside %s before using or on command line\n"%sys.argv[0])
        parser.print_help()
        sys.exit(1)

    if username == "" and options.u is not None:
        username = options.u
    elif username == "" and options.u is None:
        print( "Please set SMTP username!")
        sys.exit(1)

    if password == "":
        from getpass import getpass
        password = getpass("Password:")

    if options.sqlite is not None and options.table is not None:
        sqlfile = options.sqlite
        sqltable = options.table
    elif options.sqlite is not None and options.table is None:
        print("sqlite option requires table_name to monitor")
        sys.exit(1)
    elif options.sqlite is None and options.table is not None:
        print("table_name option requires sqlite.db to monitor")
        sys.exit(1)

    #if is_valid_number(options.phone):
    if checkvalidNumber(options.phone):

            # set the phone number color to yellow so it stands out in the output
            yellow_phone = colored(options.phone, 'yellow')

            # check if any carriers are set to true
            if True in vars(options).values():

                    if options.att or options.all:    # determine carrier email to send to and color output
                        carrier_email = '@txt.att.net'
                        color_carrier = colored("AT&T", 'blue')
                        if options.m is not None:
                            if options.file is not None:
                                watch_file = options.file
                                # also call custom action function
                                watcher = Watcher(watch_file,None )
                                watcher.watch()  # start the watch going
                            elif options.sqlite is not None:
                                watch_sqldb = options.sqlite
                                # also call custom action function
                                watcher = Watcher(None,watch_sqldb)
                                watcher.watch()  # start the watch going
                            else:
                                send_email(options.phone, carrier_email, options.m)
                        else:
                            carrier_email = colored(carrier_email, 'blue')
                            print("The %s gateway is: %s" % (color_carrier, carrier_email))
                    if options.verizon or options.all:
                        carrier_email = '@vtext.com'
                        color_carrier = colored("Verizon", 'red')
                        if options.m is not None:
                            if options.file is not None:
                                watch_file = options.file
                                # also call custom action function
                                watcher = Watcher(watch_file,None )
                                watcher.watch()  # start the watch going
                            elif options.sqlite is not None:
                                watch_sqldb = options.sqlite
                                # also call custom action function
                                watcher = Watcher(None,watch_sqldb)
                                watcher.watch()  # start the watch going
                            else:
                                send_email(options.phone, carrier_email, options.m)
                        else:
                            carrier_email = colored(carrier_email, 'red')
                            print("The %s gateway is: %s" % (color_carrier, carrier_email))
                    if options.tmobile or options.all:
                        carrier_email = '@tmomail.net'
                        color_carrier = colored("T-Mobile", 'magenta')
                        if options.m is not None:
                            if options.file is not None:
                                watch_file = options.file
                                # also call custom action function
                                watcher = Watcher(watch_file,None )
                                watcher.watch()  # start the watch going
                            elif options.sqlite is not None:
                                watch_sqldb = options.sqlite
                                # also call custom action function
                                watcher = Watcher(None,watch_sqldb)
                                watcher.watch()  # start the watch going
                            else:
                                send_email(options.phone, carrier_email, options.m)
                        else:
                            carrier_email = colored(carrier_email, 'magenta')
                            print("The %s gateway is: %s" % (color_carrier, carrier_email))
                    if options.sprint or options.all:
                        carrier_email = '@messaging.sprintpcs.com'
                        color_carrier = colored("Sprint", 'yellow')
                        if options.m is not None:
                            if options.file is not None:
                                watch_file = options.file
                                # also call custom action function
                                watcher = Watcher(watch_file,None )
                                watcher.watch()  # start the watch going
                            elif options.sqlite is not None:
                                watch_sqldb = options.sqlite
                                # also call custom action function
                                watcher = Watcher(None,watch_sqldb)
                                watcher.watch()  # start the watch going
                            else:
                                send_email(options.phone, carrier_email, options.m)
                        else:
                            carrier_email = colored(carrier_email, 'yellow')
                            print("The %s gateway is: %s" % (color_carrier, carrier_email))
                    if options.google or options.all:
                        carrier_email = '@txt.voice.google.com'
                        color_carrier = colored("Google", 'white')
                        if options.m is not None:
                            if options.file is not None:
                                watch_file = options.file
                                # also call custom action function
                                watcher = Watcher(watch_file,None )
                                watcher.watch()  # start the watch going
                            elif options.sqlite is not None:
                                watch_sqldb = options.sqlite
                                # also call custom action function
                                watcher = Watcher(None,watch_sqldb)
                                watcher.watch()  # start the watch going
                            else:
                                send_email(options.phone, carrier_email, options.m)
                        else:
                            carrier_email = colored(carrier_email, 'white')
                            print("The %s gateway is: %s" % (color_carrier, carrier_email))
                    if options.cricket or options.all:
                        carrier_email = '@sms.cricketwireless.net'
                        color_carrier = colored("Cricket", 'green')
                        if options.m is not None:
                            if options.file is not None:
                                watch_file = options.file
                                # also call custom action function
                                watcher = Watcher(watch_file,None )
                                watcher.watch()  # start the watch going
                            elif options.sqlite is not None:
                                watch_sqldb = options.sqlite
                                # also call custom action function
                                watcher = Watcher(None,watch_sqldb)
                                watcher.watch()  # start the watch going
                            else:
                                send_email(options.phone, carrier_email, options.m)
                        else:
                            carrier_email = colored(carrier_email, 'green')
                            print("The %s gateway is: %s" % (color_carrier, carrier_email))

                    # exit program normally
                    sys.exit(1)
            #code.interact(local=dict(globals(), **locals())) # debug
            elif options.m is not None:
                    cprint('Options Error: ', 'red', end='')  # print out carrier information 
                    print( "The -m option requires a carrier to be set" )
                    sys.exit(1)
            else:
                    cprint('Usage Error: ', 'red', end='')  # print out carrier information 
                    print( "Please choose carrier option" )
                    sys.exit(1)
    else:
        #cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
            cprint('Number Error: ', 'red', end='')  # print out carrier information 
            cprint("Sorry that phone number is not in the correct format ex: 1234567890 ")
            sys.exit(1)
