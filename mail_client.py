import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailClient:

    def __init__(self, smtp, imap):
        self.smtp = smtp
        self.imap = imap

    def send_message(self, sender_mail: str, password: str, subject: str, recipients: str, message: str):
        msg = MIMEMultipart()
        msg['From'] = sender_mail
        msg['To'] = recipients
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.smtp, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()

        ms.login(sender_mail, password)

        ms.sendmail(sender_mail, recipients, msg.as_string())

        ms.quit()

    def receive_message(self, sender_mail, password, header):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(sender_mail, password)

        mail.list()
        mail.select("INBOX")

        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]

        try:
            email_message = email.message_from_string(raw_email)
        except TypeError:
            email_message = email.message_from_bytes(raw_email)

        mail.logout()

        return email_message
