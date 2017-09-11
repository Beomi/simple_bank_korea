import requests
from bs4 import BeautifulSoup as bs
import datetime
from dateutil import parser


PW_DIGITS = {
    0: "d86115f1c9b7570a440b446bd3dbea74d7c0147e",
    1: "1635fef272e62b26fe205b38468afd11ca462877",
    2: "75c021ebaf5b5ab419922a2dfac58f53727e61b6",
    3: "2adcf052a5b2c85aa8a482ae63ff55e484b12f3c",
    4: "01611b0e2ade677e72ac89661b14e4b8c3d3375f",
    5: "c256a6bc1c3d6c8a88f45dc3c5258eb5d963bae9",
    6: "63fc34875835579de27b6455417ecdc99dfd6380",
    7: "6c01409758529ce8b1dadde8aa57fa05bafecb6b",
    8: "ddc2726e688db7ad812a2d3980817d479e766553",
    9: "71ef0fee840624c13d1ac476d6f53ce8f3ccf524",
}

def get_transactions(bank_num, birthday, password, days=30):
    bank_num = str(bank_num)
    birthday = str(birthday)
    password = str(password)
    hexed_pw = ''
    days = int(days)
    for p in password:
        hexed_pw += PW_DIGITS[int(p)]

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
        'BTSESSIONID': '58F1CB34F504C27495ABCDAE58102014.Bl06',
    }

    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://bobank.kbstar.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4,la;q=0.2,da;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;  charset=UTF-8',
        'Accept': 'text/html, */*; q=0.01',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://bobank.kbstar.com/quics?page=C025255&cc=b028364:b028702&QSL=F',
        'DNT': '1',
    }

    params = (
        ('chgCompId', 'b028770'),
        ('baseCompId', 'b028702'),
        ('page', 'C025255'),
        ('cc', 'b028702:b028770'),
    )

    data = [
        ('KEYPAD_TYPE_b103b54bca43', '3'),
        ('KEYPAD_HASH_b103b54bca43', hexed_pw),
        ('KEYPAD_USEYN_b103b54bca43', 'USEYN_CHECK_NAME_49bf17a91800'),
        ('KEYPAD_INPUT_b103b54bca43', '\uBE44\uBC00\uBC88\uD638'),
        ('signed_msg', ''),
        ('\uC694\uCCAD\uD0A4', ''),
        ('\uACC4\uC88C\uBC88\uD638', bank_num),
        ('\uC870\uD68C\uC2DC\uC791\uC77C\uC790', month_before_all),
        ('\uC870\uD68C\uC885\uB8CC\uC77C', this_all),
        ('\uACE0\uAC1D\uC2DD\uBCC4\uBC88\uD638', ''),
        ('\uBE60\uB978\uC870\uD68C', 'Y'),
        ('\uC870\uD68C\uACC4\uC88C', bank_num),
        ('\uBE44\uBC00\uBC88\uD638', password),
        ('USEYN_CHECK_NAME_49bf17a91800', 'Y'),
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

    r = requests.post('https://bobank.kbstar.com/quics', headers=headers, params=params, cookies=cookies, data=data)

    soup = bs(r.text, 'html.parser')
    transactions = soup.select('#pop_contents > table.tType01 > tbody > tr')

    transaction_list = []

    for idx, value in enumerate(transactions):
        tds = value.select('td')
        if not idx % 2:
            _date = tds[0].text
            _date = _date[:10] + ' ' + _date[10:]
            date = parser.parse(_date) # 날짜: datetime
            amount = -int(tds[3].text.replace(',','')) or int(tds[4].text.replace(',','')) # 입금 / 출금액: int
            balance = int(tds[5].text.replace(',','')) # 잔고: int
            detail = dict(date=date, amount=amount, balance=balance)
        else:
            transaction_by = tds[0].text.strip() # 거래자(입금자 등): str
            tmp = dict(transaction_by=transaction_by)
            transaction_list.append({**detail, **tmp})
    return transaction_list


if __name__=='__main__':
    bank_num = input('Input your Bank Acc(only digits): ')
    birthday = input('Input your birthday(ex: 941024): ')
    password = input('Input your pw(4 digits): ')
    days = int(input('How many days do you want to know?(days): '))

    trs = get_transactions(bank_num, birthday, password, days)
    print(trs)
    
