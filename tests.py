import unittest
import os

from simple_bank_korea.kb.crawler import get_transactions
from simple_bank_korea.kb.image_checker import get_keypad_img


class KookminBankTestCase(unittest.TestCase):
    def setUp(self):
        self.phantomjs_path = 'phantomjs'
        self.bank_num = os.environ['BANK_NUM']
        self.birthday = os.environ['BIRTHDAY']
        self.password = os.environ['PASSWORD']

    def test_get_keypad_img(self):
        keypad_img = get_keypad_img(self.phantomjs_path)
        self.assertEqual(type(keypad_img), dict, 'return Value is not dict.')
        self.assertNotEqual(len(keypad_img.get('JSESSIONID')), 0, 'JSESSIONID is empty.')
        self.assertNotEqual(len(keypad_img.get('QSID')), 0, 'QSID is empty.')
        self.assertNotEqual(len(keypad_img.get('KEYMAP')), 0, 'KEYMAP is empty.')
        self.assertNotEqual(len(keypad_img.get('PW_DIGITS')), 0, 'PW_DIGITS is empty.')
        self.assertNotEqual(len(keypad_img.get('KEYPAD_USEYN')), 0, 'KEYPAD_USEYN is empty.')

    def test_get_transactions(self):
        transactions = get_transactions(
            bank_num=self.bank_num,
            birthday=self.birthday,
            password=self.password,
        )
        self.assertNotEqual(len(transactions), 0, 'Transaction list is empty!')


if __name__ == '__main__':
    unittest.main()
