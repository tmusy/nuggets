import csv
import dateutil.parser

from statement2db.model import Transaction, Account
from statement2db.database import db_session

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
    rows = parse_csv(file)
    bank = db_session.query(Account).filter_by(name='Bank').first()
    for row in rows:
        for col in row:
            try:
                dt = dateutil.parser.parse(col)
                date = dateutil.parser.parse(row[0])
                text = row[1]
                debit_amount = row[2]
                credit_amount = row[3]
                amount = 0
                debit = None
                credit = None
                if debit_amount:
                    amount = debit_amount
                    debit = bank
                elif credit_amount:
                    amount = credit_amount
                    credit = bank
                valuta_date = row[4]
                saldo = row[5]

                t = Transaction(amount,'CHF',date,text)
                t.debit = debit
                t.credit = credit
                transactions.append(t)
                db_session.add(t)
                db_session.commit()
                break
            except TypeError:
                pass

    return transactions
