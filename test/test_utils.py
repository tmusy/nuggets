__author__ = 'thierry'

from statement2db.utils import allowed_file

def test_allowed_file():
    assert(allowed_file("test.txt"))
    assert(allowed_file("test.csv"))
    assert(not allowed_file("test.pdf"))
    assert(not allowed_file("test"))
