# MailMitt

MailMitt is a tool for performing regression testing on email delivery code. 
It allows applications to send emails to an SMTP server without actual emails 
being delivered to anyone.

It also provides both a web interface and a RESTful JSON API for reviewing the 
content of the emails that you send.

Nothing is actually delivered, and any emails that MailMitt receives are just
stored in memory.

It is inspired by https://github.com/ThiefMaster/maildump, although it is 
re-written from the ground up using an asyncio-based event loop rather than gevent.

Because of this, it only runs on Python 3.5 and above, whereas MailDump only runs on 
Python 2.

## Installation


```bash 
pip3 install mailmitt
```

## Usage

`mailmitt --help`

produces a list of available command line arguments.

By default mailmitt runs its webserver on port
1080 and its SMTP server on port 1025 (both only available via localhost). If 
you want to access it from another machine, use something like this:

`mailmitt --http-ip 0.0.0.0 --smtp-ip 0.0.0.0`


## API


`GET http://localhost:1080/messages`

* Gets all emails, including their content, as a JSON tree.

`GET http://localhost:1080/messages/0.source`

* Gets the source for the first email. Replace `0` with the index of the email you wish to retrieve

`GET http://localhost:1080/messages/0.plain`

* Gets the plaintext version of the first email. 

`GET http://localhost:1080/messages/0.html`

* Gets the HTML version of the first email if it exists. 

`GET http://localhost:1080/messages/0.json`

* Gets a JSON representation of the first email.

`DELETE http://localhost:1080/messages`

* Deletes all emails from memory


## Sample Usage

Run this in one terminal:
```bash
mailmitt
```

And then in a python3 session:

```python
import requests
import smtplib
from email.message import EmailMessage

message = EmailMessage()
message['Subject'] = "Sample Subject"
message['To'] = "to@example.com"
message['From'] = "from@example.com"

message.set_content("""\
Hello
This is a sample email
""")

message.add_alternative("""
<h1>Hello</h1>
<p>This is a sample email</p>
""", subtype='html')

with smtplib.SMTP('localhost',port=1025) as smtp:
    smtp.sendmail(message['From'],message['To'],message.as_string())  

print(requests.get('http://localhost:1080/messages/0.plain').text.strip())
```


Although this example is in Python, MailMitt can be accessed from SMTP client 
libraries in any language.

```
Hello
This is a sample email
```

## Webserver
You will also be able to review your emails at http://localhost:1080/