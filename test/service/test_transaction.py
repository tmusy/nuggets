import json
from statement2db.service.transaction import app


test_app = app.test_client()


def test_get_existing_course():
    # t = Transaction('test_transaction_1')
    # db_session.add(t)
    # db_session.commit()
    # our_transaction = db_session.query(Transaction).filter_by(name='test_transaction_1').first()

    res = test_app.get('/v1.0/transactions/' + str(1))
    data = json.loads(res.data)
    assert res.status_code == 200 and data['transaction']['id'] == 1
