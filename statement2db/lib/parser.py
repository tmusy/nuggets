import csv
import dateutil.parser

from statement2db.models import Transaction, Account
from statement2db.extensions import db
from statement2db.utils import unicode_csv_reader


def parse_csv(file):
    """

    :param file:
    :return:
    """
    content = []

    with open(file, 'rb') as csv_file:
        entries = csv.reader(csv_file, delimiter=',')
        for row in entries:
            content.append(row)
    return content


def extract_transactions(file):
    transactions = []
#    rows = parse_csv(file)
    rows = unicode_csv_reader(open(file))
    bank = Account.query.filter_by(name='Bank').first()
    for row in rows:
        for col in row:
            try:
                dt = dateutil.parser.parse(col)
                date = dateutil.parser.parse(row[0])
                text = row[1]
                text = " ".join(text.split())
                debit_amount = row[2]
                credit_amount = row[3]
                amount = 0.0
                debit = None
                credit = None
                if debit_amount:
                    amount = float(debit_amount)
                    debit = bank
                elif credit_amount:
                    amount = float(credit_amount)
                    credit = bank
                valuta_date = dateutil.parser.parse(row[4])
                saldo = None
                if row[5]:
                    saldo = float(row[5])
                category = row[7]

                # check if exists
                t = Transaction.query.filter_by(description=text, date=date)\
                    .filter(Transaction.amount <= int(amount)+1, Transaction.amount >= int(amount)).first()
                if not t:
                    # create a Transaction object
                    t = Transaction(amount=amount,
                                    currency='CHF',
                                    date=date,
                                    description=text,
                                    valuta_date=valuta_date,
                                    reported_saldo=saldo,
                                    category=category)
                    t.debit = debit
                    t.credit = credit
                    transactions.append(t)
                    db.session.add(t)
                    db.session.commit()
                break
            except TypeError:
                pass

    return transactions


def extract_transactions_cs(file):
    transactions = []
#    rows = parse_csv(file)
    rows = unicode_csv_reader(open(file), delimiter=',')
    bank = Account.query.filter_by(name='Bank').first()
    for row in rows:
        for col in row:
            try:
                dt = dateutil.parser.parse(col)
                date = dateutil.parser.parse(row[0])
                name = row[5]
                text = row[10]
                text = " ".join(text.split())
                amount = float(row[6])
                debit = None
                credit = None
                if amount < 0:
                    amount = amount * -1
                    debit = bank
                else:
                    credit = bank
                valuta_date = dateutil.parser.parse(row[0])
                category = row[1]

                # check if exists
                t = Transaction.query.filter_by(name=name, description=text, date=date)\
                    .filter(Transaction.amount <= int(amount)+1, Transaction.amount >= int(amount)).first()
                if not t:
                    # create a Transaction object
                    t = Transaction(amount=amount,
                                    currency='CHF',
                                    date=date,
                                    name=name,
                                    description=text,
                                    valuta_date=valuta_date,
                                    category=category)
                    t.debit = debit
                    t.credit = credit
                    transactions.append(t)
                    db.session.add(t)
                    db.session.commit()
                break
            except TypeError:
                pass
            except ValueError:
                pass

    return transactions
