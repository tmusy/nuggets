from statement2db.lib.parser import parse_csv, extract_transactions


def test_parse():
    result = parse_csv('lib/test.csv')
    print(result)
    assert(len(result) == 5)


def test_extract_transactions():
    result = extract_transactions('lib/test.csv')
    assert result