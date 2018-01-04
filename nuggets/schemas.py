from marshmallow import Schema, fields, post_load
from nuggets.models import Account, Trx


class AccountSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    nr = fields.Integer()
    type = fields.Str()

    @post_load
    def make_account(self, data):
        return Account(**data)


class TrxSchema(Schema):
    uri = fields.Url()
    amount = fields.Method('amount_sign')
    currency = fields.Str()
    saldo = fields.Float()
    description = fields.Str()
    date = fields.DateTime()
    name = fields.Str()
    account = fields.Method('get_account')

    def amount_sign(self, obj):
        if obj.credit_id != 1:
            return -obj.amount
        return obj.amount

    def get_account(self, obj):
        if obj.credit_id == 1:
            if obj.debit:
                return obj.debit.name
        if obj.credit:
            return obj.credit.name
        return None

    @post_load
    def make_trx(self, data):
        return Trx(**data)
