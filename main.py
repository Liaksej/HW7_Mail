import configparser

from mail_client import MailClient

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("credits.ini")

    smtp_sever = config['MAIL_SERVERS']['smtp_sever']
    imap_server = config['MAIL_SERVERS']['imap_server']

    sender_mail = config['AUTHORIZATION']['sender_mail']
    password = config['AUTHORIZATION']['password']

    subject = config['DATA_FOR_SEND']['subject']
    recipients = config['DATA_FOR_SEND']['recipients']
    message = config['DATA_FOR_SEND']['message']

    if config['DATA_FOR_RECEIVE']['header'] == '':
        header = None
    else:
        header = config['DATA_FOR_RECEIVE']['header']

    mailclient = MailClient(smtp_sever, imap_server)

    mailclient.send_message(sender_mail, password, subject, recipients, message)
    print(mailclient.receive_message(sender_mail, password, header))
