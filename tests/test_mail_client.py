import pytest
import configparser

from mail_client import MailClient


class TestMailClient:

    @pytest.fixture
    def setup_teardown(self):
        config = configparser.ConfigParser()
        config.read("../credits.ini")

        self.smtp_sever = config['MAIL_SERVERS']['smtp_sever']
        self.imap_server = config['MAIL_SERVERS']['imap_server']

        self.sender_mail = config['AUTHORIZATION']['sender_mail']
        self.password = config['AUTHORIZATION']['password']

        self.subject = config['DATA_FOR_SEND']['subject']
        self.recipients = config['DATA_FOR_SEND']['recipients']
        self.message = config['DATA_FOR_SEND']['message']

        if config['DATA_FOR_RECEIVE']['header'] == '':
            self.header = None
        else:
            self.header = config['DATA_FOR_RECEIVE']['header']

        self.mailclient = MailClient(self.smtp_sever, self.imap_server)

        # mailclient.send_message(sender_mail, password, subject, recipients, message)
        # print(mailclient.receive_message(sender_mail, password, header))
        yield

    def test_receive_message(self, setup_teardown):
        assert len(self.mailclient.receive_message(self.sender_mail, self.password, self.header).defects) == 0

    def test_send_message(self, setup_teardown):
        with pytest.raises(Exception):
            assert not (self.mailclient.send_message(self.sender_mail, self.password, self.subject, self.sender_mail,
                                                     self.message))


if __name__ == '__main__':
    TestMailClient()
