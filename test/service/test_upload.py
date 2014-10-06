from statement2db.service.upload import app, allowed_file

test_app = app.test_client()


def test_allowed_file():
    assert(allowed_file("test.txt"))
    assert(allowed_file("test.csv"))
    assert(not allowed_file("test.pdf"))
    assert(not allowed_file("test"))


def test_do_the_upload():
    pass


def test_post_upload():
    with open('service/test.csv', 'rb') as testfile:
        res = test_app.post('/v1.0/import/transactions', data= {'file': testfile})
        assert res.status_code == 200
        res = test_app.post('/v1.0/import/transactions', data= {'file': None})
        assert res.status_code == 400
