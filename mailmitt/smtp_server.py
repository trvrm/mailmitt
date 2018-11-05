import datetime
import email.header
import email
import asyncio
import aiosmtpd.smtp

messages = []
"""
    We don't currently provide any kind of serialization mechanism - all
    email data is simply held in memory in this data structure.
"""


def decode_header(header):
    return str(email.header.make_header(email.header.decode_header(header)))


def extract_part(part):
    charset = part.get_content_charset()
    return {
        "type": part.get_content_type(),
        "is_attachment": part.get_filename() is not None,
        "filename": part.get_filename(),
        "charset": part.get_content_charset(),
        "body": part.get_payload(decode=True).decode(charset),
    }


class Handler:
    async def handle_DATA(self, server, session, envelope):
        print("Message from {}".format(envelope.mail_from))

        message = email.message_from_string(envelope.content)

        # should compute plain/html here.
        messages.append(
            {
                "sender": envelope.mail_from,
                "recipients": {"to": envelope.rcpt_tos},
                "subject": decode_header(message["subject"]),
                "source": envelope.content,
                "created_at": datetime.datetime.now().isoformat(" "),
                "type": message.get_content_type(),
                "size": len(envelope.content),
                "parts": [
                    extract_part(part)
                    for part in message.walk()
                    if not part.is_multipart()
                ],
            }
        )

        return "250 Message accepted for delivery"


def factory():
    loop = asyncio.get_event_loop()
    # Errors here failing silently unfortunately
    return aiosmtpd.smtp.SMTP(
        Handler(), enable_SMTPUTF8=True, loop=loop, decode_data=True
    )
