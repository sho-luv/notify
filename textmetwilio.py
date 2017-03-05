# /usr/bin/env python
import argparse # Parser for command-line options, arguments and sub-commands
import smtplib	# SMTP protocol client
from twilio.rest.lookups import TwilioLookupsClient # twilio api used to enumerate carrier
from twilio.rest.exceptions import TwilioRestException # twilio exception handler for error handling
import sys # used sys to have clean exits of the program
import os # used to call sendEmail because I didn't want to use python smtplib ....
import subprocess # used to call sendEmail because I didn't want to use python's smtplib ....
from termcolor import colored, cprint # used to print colors

# python -m pdb textmetwilio.py # debug program
###############################################
# by sho.luv:
# This progam uses carriers gateways to 
# to convert emails to sms messages to phone numbers
#
###############################################

parser = argparse.ArgumentParser(description='This program sends text messages to people using by using email.')
parser.add_argument('phone', action='store', help='Phone number to send text message to')
parser.add_argument('-m', action='store', metavar = '"text message"', help='Text message')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

options = parser.parse_args()
# Download the Python helper library from twilio.com/docs/python/install
# Your Account Sid and Auth Token from twilio.com/user/account
# Store them in the environment variables:
# "TWILIO_ACCOUNT_SID" and "TWILIO_AUTH_TOKEN"
# Find these values at https://twilio.com/user/account

# Twilio Account information
#################################################################
account_sid = "" # stolen account_sid
auth_token = ""	# stolen auth_token
#################################################################
# check settings before trying to use
if not account_sid or not auth_token:
	print "Please set Twilio settings inside %s before using..."%sys.argv[0]

# SMTP settings server and credentials
#################################################################
smtp_server = 'mail.smtp.com'	# gmail smtp: smtp.gmail.com					
smtp_port = '2525'				# gmail port: 587
email_from = 'your@computer.com'
email_subject = 'Alert'
username = ''    		# username
password = '' # password 
#password = '' # password 
#################################################################
# check settings before trying to use
if not username or not password:
    print "Please set SMTP settings inside %s before using..."%sys.argv[0]
    sys.exit(1)

# Twilio Authentication:
client = TwilioLookupsClient(account_sid, auth_token)

def is_valid_number(number):
    try:
        response = client.phone_numbers.get(number, include_carrier_info=True)
        response.phone_number  # If invalid, throws an exception.
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e

if is_valid_number(options.phone):
	number = client.phone_numbers.get(options.phone, include_carrier_info=True)
	yellow_phone = colored(options.phone, 'yellow')
	if options.m is not None:

		if 'AT&T' in number.carrier['name']:	# determine carrier email to send to and color output
			carrier_email = 'txt.att.net'
			color_carrier = colored(number.carrier['name'], 'blue')
		elif 'Verizon' in number.carrier['name']:
			carrier_email = 'vtext.com'
			color_carrier = colored(number.carrier['name'], 'red')
		elif 'T-Mobile' in number.carrier['name']:
			carrier_email = 'tmomail.net'
			color_carrier = colored(number.carrier['name'], 'magenta')
		elif 'Sprint' in number.carrier['name']:
			carrier_email = 'messaging.sprintpcs.com'
			color_carrier = colored(number.carrier['name'], 'yellow')
		elif 'Google' in number.carrier['name']:
			carrier_email = 'txt.voice.google.com'
			color_carrier = colored(number.carrier['name'], 'white')
		elif 'Cricket' in number.carrier['name']:
			carrier_email = 'sms.cricketwireless.net'
			color_carrier = colored(number.carrier['name'], 'green')
		else:
			print "Sorry I don't know who your carrier is..."
			sys.exit(1)

		email = "sendEmail -f %s -t %s@%s -u %s "\
			 "-s %s:%s -o tls=yes -xu %s -xp %s -m %s"\
			 % (email_from, options.phone, carrier_email, email_subject, smtp_server, smtp_port, username, password, options.m)
		
		output = subprocess.check_output(email, shell=True) # call to os to run command and save ouput

		if 'successfully' in output:
			cprint('[+] ', 'green', attrs=['bold'], end='')  # print success
			cprint(output[0:16], end='')	# print out date and timestamp of message sent
			response = " Message sent to %s on the %s network" % (yellow_phone, color_carrier)
			print(response)  
		else:
				cprint("Sorry unable to send message...", 'red', attrs=['bold'])
	else:
		cprint(number.carrier['name'], 'green', attrs=['bold'])  # print out carrier information 
        sys.exit(1)
else:
    cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
    cprint("Sorry that phone number isn't valid ", end='')
    cprint(':( ', 'yellow', attrs=['bold'])  # print success
    sys.exit(1)
    
