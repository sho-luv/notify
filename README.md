<p align="center">
<img width="459" alt="notify" src="https://user-images.githubusercontent.com/1679089/80288703-8b8f8a80-86ee-11ea-92b0-5b2c6263c463.png">

</p>

<h4 align="center">Notification Application</h4>
<p align="center">
  <a href="https://twitter.com/sho_luv">
  <img src="https://img.shields.io/badge/Twitter-%40sho_luv-blue.svg">
  </a>
</p>


# notify.py

This is a python script for sending text message via the ISP's email gateway to a phone number in the form of email to text.
Additionally this script can be used to monitor a changes in a file. Currently it supports:

- modification time (mtime) of a specified file with the -file flag
- sqlite database table row count. If the count changes a notification is sent with the -sqlite and -table flags


## Usage of notify.py
```
usage: notify.py [-h] [-m "msg"] [-u username] [-att] [-cricket] [-google]
                 [-sprint] [-tmobile] [-verizon] [-all] [-file File]
                 [-sqlite sqlite.db] [-table table_name]
                 phone

This program sends text messages to people using by using email.

positional arguments:
  phone              Phone number to send text message to. Phone number should
                     have no spaces and be of format ##########

optional arguments:
  -h, --help         show this help message and exit
  -m "msg"           Text message
  -u username        SMTP username

carrier:
  -att               Send text message to AT&T Wireles
  -cricket           Send text message to Cricket
  -google            Send text message to Google
  -sprint            Send text message to Sprint
  -tmobile           Send text message to T-Mobile
  -verizon           Send text message to Verizon Wireless
  -all               Send text message to all networks

Notify options:
  -file File         Send notification if file changes
  -sqlite sqlite.db  Send notification if table in sqlite.db changes also
                     requires -table option
  -table table_name  Send notification if table in sqlite.db changes

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
python notify.py xxxxxxxxxx -att -m "File has changed" -file requirements.txt -u <username>
Password:
[+] Notification set to watch file: requirements.txt
[+] Apr 17 05:37:05  Message sent to xxxxxxxxxx on the AT&T network

```
## Example of notify.py monitoring file
```
python notify.py xxxxxxxxxx -google -sqlite file.db -table admins -m "File has changed" -u <username>
Password:
[+] Notification set to watch file: file.db
[+] Apr 16 06:24:09  Message sent to xxxxxxxxxx on the Google network

```
