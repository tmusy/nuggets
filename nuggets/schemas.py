from marshmallow import Schema, fields, post_load
from marshmallow_sqlalchemy import ModelSchema
from nuggets.models import Account, Trx
from nuggets.extensions import db


class BaseSchema(ModelSchema):
    class Meta:
        sqla_session = db.session


class AccountSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Account


class TrxSchema(BaseSchema):
    credit = fields.Nested(AccountSchema)
    debit = fields.Nested(AccountSchema)

    class Meta:
        fields = ("id", "amount", "currency", "date", "name", "description", "saldo", "credit", "debit")


class TrxByAccountSchema(TrxSchema):
    account = fields.Method('get_account')
    type = fields.Method('get_type')

    class Meta:
        fields = ("id", "amount", "currency", "date", "name", "description", "saldo", "credit", "debit", "account", "type")

    def get_account(self, obj):
        if obj.credit_id == 1:
            if obj.debit:
                return obj.debit.name
        if obj.debit_id == 1:
            if obj.credit:
                return obj.credit.name
        return None

    def get_type(self, obj):
        if obj.credit_id == 1:
            return 'income'
        return 'expense'

    @post_load
    def make_trx(self, data):
        return Trx(**data)
