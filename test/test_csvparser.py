import statement2db.csvparser


def test_parse():
    result = csvparser.parse('test.csv')
    print(result)