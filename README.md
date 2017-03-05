# notify


##Usage
```
python textmetwilio.py 
usage: textmetwilio.py [-h] [-m "text message"] phone

This program sends text messages to people using by using email.

positional arguments:
  phone              Phone number to send text message to

optional arguments:
  -h, --help         show this help message and exit
  -m "text message"  Text message
root@Id10t:~/work/mydev/notify# 
root@Id10t:~/work/mydev/notify# python textmetwilio.py 2108183364
AT&T Wireless
root@Id10t:~/work/mydev/notify# python textmetwilio.py 2108183364 -m "Hi"
[+] Mar 05 04:40:14  Message sent to 2108183364 on the AT&T Wireless network
root@Id10t:~/work/mydev/notify# 
```
