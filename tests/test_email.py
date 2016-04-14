import sys
import unittest
from mock import *
from faker import Factory


my_dict = dict()


def getitem(name):
    return my_dict[name]


def setitem(name, val):
    my_dict[name] = val

MimeText = MagicMock(name="MimeText")
MimeText.__getitem__.side_effect = getitem
MimeText.__setitem__.side_effect = setitem
sys.modules["email.mime.text"] = MimeText


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.fake = Factory.create()

    def tearDown(self):
        pass

    def test_send(self):
        sender = self.fake.email()
        recipient = self.fake.email()
        subject = self.fake.words(nb=3)
        body = self.fake.text(max_nb_chars=200)

        serverMock = Mock(spec=["sendmail", "quit"])
        serverMock.sendmail.return_value = True

        smtpMock = Mock(name="SMTP")
        smtpMock.SMTP.return_value = serverMock
        sys.modules["smtplib"] = smtpMock

        import utils.emailUtil as emailUtil
        self.assertTrue(emailUtil.send(sender, recipient, subject, body))

        # check for mock calls
        self.assertEqual(smtpMock.SMTP.call_count, 1, "Unexpected calls amount")
        self.assertEqual(serverMock.sendmail.call_count, 1, "Unexpected calls amount")
        self.assertEqual(serverMock.quit.call_count, 1, "Unexpected calls amount")

        # reset mock internal state
        smtpMock.reset_mock()
        serverMock.reset_mock()

        serverMock.sendmail.side_effect = KeyError("foo")
        smtpMock.SMTP.return_value = serverMock
        sys.modules["smtplib"] = smtpMock

        reload(emailUtil)
        self.assertFalse(emailUtil.send(sender, recipient, subject, body))

        # check for mock calls
        self.assertEqual(smtpMock.SMTP.call_count, 1, "Unexpected calls amount")
        self.assertEqual(serverMock.sendmail.call_count, 1, "Unexpected calls amount")
        self.assertEqual(serverMock.quit.call_count, 1, "Unexpected calls amount")

