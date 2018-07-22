# notify scripts

There are two python scripts for sending text message, and an example of using the scripts inside of another program to get notified of an event.

## Textmetwilio.py
This script uses the Twilio API. To use the Twilio API you will need to register at https://www.twilio.com/ and obtain a tokens which you will need to enter in the textmetwilio.py script in the following locations:

```
Twilio Account information
#################################################################
account_sid = ""
auth_token = ""
#################################################################
```
## Usage of textmetwilio.py
```
python textmetwilio.py
usage: textmetwilio.py [-h] [-m "text message"] phone

This program sends text messages to people by using email.

positional arguments:
  phone              Phone number to send text message to

optional arguments:
  -h, --help         show this help message and exit
  -m "text message"  Text message
```
## Example of textmetwilio.py
```
python textmetwilio.py xxxxxxxxxx
AT&T Wireless

python textmetwilio.py xxxxxxxxx1
Sprint Spectrum, L.P.

python textmetwilio.py xxxxxxxxx2
Metro PCS, Inc.


python textmetwilio.py xxxxxxxxxx -m "Hi"
[+] Mar 05 04:40:14  Message sent to xxxxxxxxxx on the AT&T Wireless network

```
## Usage of notify.py
```
python notify.py
usage: notify.py [-h] [-m] [-att] [-cricket] [-google] [-sprint]
                         [-tmobile] [-verizon] [-all]
                         phone

This program sends text messages to people using by using email.

positional arguments:
  phone       Phone number to send text message to. Phone number should have
              no spaces and be of format ##########

optional arguments:
  -h, --help  show this help message and exit
  -m          "Text message"

carrier:
  -att        Send text message to AT&T Wireles
  -cricket    Send text message to Cricket
  -google     Send text message to Google
  -sprint     Send text message to Sprint
  -tmobile    Send text message to T-Mobile
  -verizon    Send text message to Verizon Wireless
  -all        Send text message to all networks

```
## Example of notify.py
```
python notify.py xxxxxxxxxx -m 'Hello there buddy!' -all

[+] Jul 20 16:56:24  Message sent to xxxxxxxxxx on the AT&T network
[+] Jul 20 16:56:26  Message sent to xxxxxxxxxx on the Verizon network
[+] Jul 20 16:56:28  Message sent to xxxxxxxxxx on the T-Mobile network
[+] Jul 20 16:56:29  Message sent to xxxxxxxxxx on the Sprint network
[+] Jul 20 16:56:31  Message sent to xxxxxxxxxx on the Google network
[+] Jul 20 16:56:32  Message sent to xxxxxxxxxx on the Cricket network
```
The logic in sending it to all carriers is that its going to find its way to the person you want it to as the number will only be serviced by one of these carriers in the united states. No international services yet covered by these scipts that I know of.
