from statement2db.lib.parser import parse_csv


def test_parse():
    result = parse_csv('lib/test.csv')
    print(result)
    assert(len(result) == 4)
