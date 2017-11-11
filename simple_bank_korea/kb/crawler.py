import requests
from bs4 import BeautifulSoup as bs
import datetime
from dateutil import parser
import os
import json

from .image_checker import get_keypad_img

from simple_bank_korea.libcheck.phantomjs_checker import TMP_DIR, get_phantomjs_path


def get_transactions(bank_num, birthday, password, days=30,
                     PHANTOM_PATH=get_phantomjs_path(),
                     LOG_PATH=os.path.devnull):
    def _get_transactions(VIRTUAL_KEYPAD_INFO, bank_num, birthday, password, days, PHANTOM_PATH, LOG_PATH):
        PW_DIGITS = VIRTUAL_KEYPAD_INFO['PW_DIGITS']
        KEYMAP = VIRTUAL_KEYPAD_INFO['KEYMAP']
        JSESSIONID = VIRTUAL_KEYPAD_INFO['JSESSIONID']
        QSID = VIRTUAL_KEYPAD_INFO['QSID']
        KEYPAD_USEYN = VIRTUAL_KEYPAD_INFO['KEYPAD_USEYN']

        bank_num = str(bank_num)
        birthday = str(birthday)
        password = str(password)
        hexed_pw = ''
        days = int(days)
        for p in password:
            hexed_pw += PW_DIGITS[str(p)]

        today = datetime.datetime.today()
        this_year = today.strftime('%Y')
        this_month = today.strftime('%m')
        this_day = today.strftime('%d')
        this_all = today.strftime('%Y%m%d')

        month_before = today - datetime.timedelta(days=days)

        month_before_year = month_before.strftime('%Y')
        month_before_month = month_before.strftime('%m')
        month_before_day = month_before.strftime('%d')
        month_before_all = month_before.strftime('%Y%m%d')

        cookies = {
            '_KB_N_TIKER': 'N',
            'JSESSIONID': JSESSIONID,
            'QSID': QSID,
            'delfino.recentModule': 'G3',
        }

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'https://obank.kbstar.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4,la;q=0.2,da;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;  charset=UTF-8',
            'Accept': 'text/html, */*; q=0.01',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://obank.kbstar.com/quics?page=C025255&cc=b028364:b028702&QSL=F',
            'DNT': '1',
        }

        params = (
            ('chgCompId', 'b028770'),
            ('baseCompId', 'b028702'),
            ('page', 'C025255'),
            ('cc', 'b028702:b028770'),
        )

        data = [
            ('KEYPAD_TYPE_{}'.format(KEYMAP), '3'),
            ('KEYPAD_HASH_{}'.format(KEYMAP), hexed_pw),
            ('KEYPAD_USEYN_{}'.format(KEYMAP), KEYPAD_USEYN),
            ('KEYPAD_INPUT_{}'.format(KEYMAP), '\uBE44\uBC00\uBC88\uD638'),
            ('signed_msg', ''),
            ('\uC694\uCCAD\uD0A4', ''),
            ('\uACC4\uC88C\uBC88\uD638', bank_num),
            ('\uC870\uD68C\uC2DC\uC791\uC77C\uC790', month_before_all),
            ('\uC870\uD68C\uC885\uB8CC\uC77C', this_all),
            ('\uACE0\uAC1D\uC2DD\uBCC4\uBC88\uD638', ''),
            ('\uBE60\uB978\uC870\uD68C', 'Y'),
            ('\uC870\uD68C\uACC4\uC88C', bank_num),
            ('\uBE44\uBC00\uBC88\uD638', password),
            ('USEYN_CHECK_NAME_{}'.format(KEYMAP), 'Y'),
            ('\uAC80\uC0C9\uAD6C\uBD84', '2'),
            ('\uC8FC\uBBFC\uC0AC\uC5C5\uC790\uBC88\uD638', birthday),
            ('\uC870\uD68C\uC2DC\uC791\uB144', month_before_year),
            ('\uC870\uD68C\uC2DC\uC791\uC6D4', month_before_month),
            ('\uC870\uD68C\uC2DC\uC791\uC77C', month_before_day),
            ('\uC870\uD68C\uB05D\uB144', this_year),
            ('\uC870\uD68C\uB05D\uC6D4', this_month),
            ('\uC870\uD68C\uB05D\uC77C', this_day),
            ('\uC870\uD68C\uAD6C\uBD84', '2'),
            ('\uC751\uB2F5\uBC29\uBC95', '2'),
        ]

        r = requests.post('https://obank.kbstar.com/quics', headers=headers, params=params, cookies=cookies, data=data)

        soup = bs(r.text, 'html.parser')

        transactions = soup.select('#pop_contents > table.tType01 > tbody > tr')

        transaction_list = []

        for idx, value in enumerate(transactions):
            tds = value.select('td')
            if not idx % 2:
                _date = tds[0].text
                _date = _date[:10] + ' ' + _date[10:]
                date = parser.parse(_date)  # 날짜: datetime
                amount = -int(tds[3].text.replace(',', '')) or int(tds[4].text.replace(',', ''))  # 입금 / 출금액: int
                balance = int(tds[5].text.replace(',', ''))  # 잔고: int
                detail = dict(date=date, amount=amount, balance=balance)
            else:
                transaction_by = tds[0].text.strip()  # 거래자(입금자 등): str
                tmp = dict(transaction_by=transaction_by)
                transaction_list.append({**detail, **tmp})
        return transaction_list

    VIRTUAL_KEYPAD_INFO_JSON = os.path.join(TMP_DIR, 'kb_{}.json'.format(bank_num))
    if os.path.exists(VIRTUAL_KEYPAD_INFO_JSON):
        fp = open(VIRTUAL_KEYPAD_INFO_JSON)
        VIRTUAL_KEYPAD_INFO = json.load(fp)
        fp.close()
    else:
        VIRTUAL_KEYPAD_INFO = get_keypad_img(PHANTOM_PATH, LOG_PATH)
        fp = open(VIRTUAL_KEYPAD_INFO_JSON, 'w+')
        json.dump(VIRTUAL_KEYPAD_INFO, fp)
        fp.close()

    result = _get_transactions(VIRTUAL_KEYPAD_INFO, bank_num, birthday, password, days, PHANTOM_PATH, LOG_PATH)
    if result:
        return result
    else:
        print('Session Expired! Get new touch keys..')
        NEW_VIRTUAL_KEYPAD_INFO = get_keypad_img(PHANTOM_PATH, LOG_PATH)
        fp = open(VIRTUAL_KEYPAD_INFO_JSON, 'w+')
        json.dump(NEW_VIRTUAL_KEYPAD_INFO, fp)
        fp.close()
        return _get_transactions(NEW_VIRTUAL_KEYPAD_INFO, bank_num, birthday, password, days, PHANTOM_PATH, LOG_PATH)


if __name__ == '__main__':
    bank_num = input('Input your Bank Acc(only digits): ')
    birthday = input('Input your birthday(ex: 941024): ')
    password = input('Input your pw(4 digits): ')
    days = int(input('How many days do you want to know?(days): '))
    trs = get_transactions(bank_num, birthday, password, days)
    print(trs)
