# notify.py

This is a python script for sending text message via the ISP's email gateway to a persons phone in the form of email to text.
Additionally this script can be used to monitor a change in modification time (mtime) of a specified file.


## Usage of notify.py
```
usage: notify.py [-h] [-m] [-u username] [-att] [-cricket] [-google] [-sprint]
                 [-tmobile] [-verizon] [-all] [-n File]
                 phone

This program sends text messages to people using by using email.

positional arguments:
  phone        Phone number to send text message to. Phone number should have
               no spaces and be of format ##########

optional arguments:
  -h, --help   show this help message and exit
  -m           "Text message"
  -u username  SMTP username

carrier:
  -att         Send text message to AT&T Wireles
  -cricket     Send text message to Cricket
  -google      Send text message to Google
  -sprint      Send text message to Sprint
  -tmobile     Send text message to T-Mobile
  -verizon     Send text message to Verizon Wireless
  -all         Send text message to all networks

Notify options:
  -n File      Send notification if file changes


```
## Example of notify.py sending text message
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

## Example of notify.py monitoring file
```
python notify.py xxxxxxxxxx -att -m "File has changed" -n requirements.txt -u <username>
Password:
[+] Notification set to watch file: requirements.txt
[+] Apr 17 05:37:05  Message sent to xxxxxxxxxx on the AT&T network

```
