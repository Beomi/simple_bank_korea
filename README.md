# Simple Bank Korea

## Simplest Transaction Crawler for Korea Banks

Requirements:

- bs4 (BeautifulSoup4)
- requests
- python-dateutil

## Install

Install package with pip:

```bash
pip install simple_bank_korea
```

## KB (Kookmin Bank)

Currently supports KB국민은행(Kookmin Bank) only.

### Before Use

You must activate '빠른조회' service for each banks.

> check this: https://obank.kbstar.com/quics?page=C025255&cc=b028364:b028702&QSL=F#

You can only use service('빠른조회')-registered bank accounts.

### Usage

Import functions from each bank:

```python
from simple_bank_korea.kb import get_transactions

# get_transactions returns list of dicts
# like this:
# [{'transaction_by': '', 'date': datetime.datetime(2017, 9, 11, 12, 39, 42), 'amount': 50, 'balance': 394}]

# example
transaction_list = get_transactions(
        bank_num='47380204123456',
        birthday='941021',
        password='5432',
        # days=30, # Optional, default is 30
    )

for trs in transaction_list:
    print(trs['date'], trs['amount'], trs['transaction_by'])
```

`get_transactions()` needs `bank_num`, `birthday` and `password`. and optionally you can use `days` arg for specific days from today.(default is 30days(1month))

#### Require Args

- `bank_num`: Your account number. (String)
- `birthday`: Your birthday with birth year(if 1994/10/21, do '941021'), 6 digits. (String)
- `password`: Your bank account password. (String)

#### Optional Args

- `days`: Days you want to get datas. Default is 30 days. (Integer)

#### Return types

`get_transactions()` returns list of dicts, and each dict has `date`, `amount`, `balance` and `transaction_by`.

- `get_transactions()`: returns list of transaction dicts.

- `date`: datetime
- `amount`: int
- `balance`: int
- `transaction_by`: str


