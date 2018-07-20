# /usr/bin/env python
import argparse # Parser for command-line options, arguments and sub-commands
import smtplib	# SMTP protocol client
from twilio.rest.lookups import TwilioLookupsClient # twilio api used to enumerate carrier
from twilio.rest.exceptions import TwilioRestException # twilio exception handler for error handling
import code # used for debugging with the command "code.interact(local=dict(globals(), **locals()))
import sys # used sys to have clean exits of the program
import smtplib # used to send email so we can do email to text
import os # used to call sendEmail because I didn't want to use python smtplib ....
import subprocess # used to call sendEmail because I didn't want to use python smtplib ....
from termcolor import colored, cprint

# python -m pdb email-to-sms.py # debug program
######################
#
# This progam uses an email address
# to send sms messages to phone numbers
#

parser = argparse.ArgumentParser(description='This program sends text messages to people using by using email.')
parser.add_argument('phone', action='store', metavar='phone',help="Phone number to send text message to.\n Phone number should have no spaces and be of format ##########")
parser.add_argument('-m', action='store', metavar = '', help='"Text message"')

#group = parser.add_mutually_exclusive_group()
group = parser.add_argument_group('carrier')

group.add_argument('-att', action='store_true', help='Send text message to AT&T Wireles')
group.add_argument('-cricket', action='store_true', help='Send text message to Cricket')
group.add_argument('-google', action='store_true', help='Send text message to Cricket')
group.add_argument('-sprint', action='store_true', help='Send text message to Sprint')
group.add_argument('-tmobile', action='store_true',  help='Send text message to T-Mobile')
group.add_argument('-verizon', action='store_true', help='Send text message to Verizon Wireless')
group.add_argument('-all', action='store_true', help='Send text message to all networks')

#code.interact(local=dict(globals(), **locals())) # debug

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

options = parser.parse_args()

def is_valid_number(number):
    if len(number) != 10 and number.isdigit():
	return False
    else:
	return True

def send_email(number, carrier_email, message):

	# SMTP settings server and credentials
	#################################################################
	smtp_server = 'mail.smtp.com'	# gmail smtp: smtp.gmail.com								
	smtp_port = '2525'				# gmail port: 587
	email_subject = 'Alert'
	username = ''    		# username
	password = '' # password 
	#password = '' # password 
	#################################################################
	if not username or not password:
		print "Please set SMTP settings inside %s before using..."%sys.argv[0]
		sys.exit(1)

	email = "sendEmail -f your@computer.com -t %s%s -u Alert "\
		"-s %s:%s -o tls=yes -xu %s -xp %s -m %s"\
		% (number, carrier_email, smtp_server, smtp_port, username, password, message)
	try:
		output = subprocess.check_output(email, shell=True) # call to os to run command and save ouput
	except Exception, e:
		cprint('Email Send Error: ', 'red', end='')  # print out carrier information 
 		print str(e)
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

if is_valid_number(options.phone):
	# set the phone number color to yellow so it stands out in the output
	yellow_phone = colored(options.phone, 'yellow')
	# check to see if there is a message being sent

	# check if any carriers are set to true
	if True in vars(options).values():

		if options.att or options.all:    # determine carrier email to send to and color output
			carrier_email = '@txt.att.net'
			color_carrier = colored("AT&T", 'blue')
			if options.m is not None:
				send_email(options.phone, carrier_email, options.m)
			else:
				carrier_email = colored(carrier_email, 'blue')
				print"The %s gateway is: %s"%(color_carrier, carrier_email)
		if options.verizon or options.all:
			carrier_email = '@vtext.com'
			color_carrier = colored("Verizon", 'red')
			if options.m is not None:
				send_email(options.phone, carrier_email, options.m)
			else:
				carrier_email = colored(carrier_email, 'red')
				print"The %s gateway is: %s"%(color_carrier, carrier_email)
		if options.tmobile or options.all:
			carrier_email = '@tmomail.net'
			color_carrier = colored("T-Mobile", 'magenta')
			if options.m is not None:
				send_email(options.phone, carrier_email, options.m)
			else:
				carrier_email = colored(carrier_email, 'magenta')
				print"The %s gateway is: %s"%(color_carrier, carrier_email)
		if options.sprint or options.all:
			carrier_email = '@messaging.sprintpcs.com'
			color_carrier = colored("Sprint", 'yellow')
			if options.m is not None:
				send_email(options.phone, carrier_email, options.m)
			else:
				carrier_email = colored(carrier_email, 'yellow')
				print"The %s gateway is: %s"%(color_carrier, carrier_email)
		if options.google or options.all:
			carrier_email = '@txt.voice.google.com'
			color_carrier = colored("Google", 'white')
			if options.m is not None:
				send_email(options.phone, carrier_email, options.m)
			else:
				carrier_email = colored(carrier_email, 'white')
				print"The %s gateway is: %s"%(color_carrier, carrier_email)
		if options.cricket or options.all:
			carrier_email = '@sms.cricketwireless.net'
			color_carrier = colored("Cricket", 'green')
			if options.m is not None:
				send_email(options.phone, carrier_email, options.m)
			else:
				carrier_email = colored(carrier_email, 'green')
				print"The %s gateway is: %s"%(color_carrier, carrier_email)

		# exit program normally
		sys.exit(1)
	#code.interact(local=dict(globals(), **locals())) # debug
	elif options.m is not None:
		cprint('Options Error: ', 'red', end='')  # print out carrier information 
		print "The -m option requires a carrier to be set"
		sys.exit(1)
	else:
		cprint('Usage Error: ', 'red', end='')  # print out carrier information 
		print "Please choose carrier option"
		sys.exit(1)
else:
    #cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
	cprint('Number Error: ', 'red', end='')  # print out carrier information 
	cprint("Sorry that phone number is not in the correct format ex: 1234567890 ")
	sys.exit(1)
    
