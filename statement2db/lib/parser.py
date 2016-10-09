import csv
import dateutil
import datetime

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
                name, text = text.split(',')
                name = name.strip()
                text = text.strip()
#                text = " ".join(text.split())
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
                #category = row[7]
                category = None

                # check if exists
                t = Transaction.query.filter_by(description=text, date=date)\
                    .filter(Transaction.amount <= int(amount)+1, Transaction.amount >= int(amount)).first()
                if not t:
                    # create a Transaction object
                    t = Transaction(amount=amount,
                                    currency='CHF',
                                    date=date,
                                    name=name,
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
            except ValueError:
                pass
            except TypeError:
                pass

    return transactions


def extract_transactions_cs(file):
    """
    Extracts transaction from the CSV export from directnet.

    :param file: utf-8 csv file from directnet (convert tu utf-8 first)
    :return:
    """
    transactions = []

    rows = unicode_csv_reader(open(file), delimiter=',')
    bank = Account.query.filter_by(name='Bank').first()
    for row in rows:
        date = to_date(row[0])
        if date:
            t = row[1].split(',')
            name = t[0].strip()
            text = t[1].strip()
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
            valuta_date = to_date(row[4])
            saldo = None
            if row[5]:
                saldo = float(row[5])

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
                                reported_saldo=saldo)
                t.debit = debit
                t.credit = credit
                transactions.append(t)
                db.session.add(t)
                db.session.commit()

    return transactions


def to_date(date_string):
    try:
        format = '%d.%m.%Y'
        d = datetime.datetime.strptime(date_string, format)
        return d
    except ValueError:
        return None
