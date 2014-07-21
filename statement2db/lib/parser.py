import csv


def parse_csv(file):
    """

    :param file:
    :return:
    """
    content = []

    with open(file, 'rb') as csvfile:
        entries = csv.reader(csvfile, delimiter=';')
        for row in entries:
            content.append(row)
    return content
