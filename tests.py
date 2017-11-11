import unittest
import os

from simple_bank_korea.kb.crawler import get_transactions
from simple_bank_korea.kb.image_checker import get_keypad_img
from simple_bank_korea.libcheck.phantomjs_checker import get_phantomjs_path


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


class LibcheckTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_phantomjs_path_if_phantomjs_in_PATH(self):
        phantomjs_path = get_phantomjs_path()
        self.assertEqual(phantomjs_path, 'phantomjs', 'PhantomJS Does not in PATH.')

    def test_get_phantomjs_path_if_phantomjs_not_in_PATH(self):
        os.environ['phantomjs'] = 'overriding_this'
        phantomjs_path = get_phantomjs_path()
        self.assertTrue('phantomjs' in phantomjs_path, 'Download PhantomJS Failed.')


if __name__ == '__main__':
    unittest.main()
