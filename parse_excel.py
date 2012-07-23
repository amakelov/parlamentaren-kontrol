import xlrd
from collections import namedtuple

rep = namedtuple('rep', ['name', 'party'])
session = namedtuple('session', ['kind', 'details'])

registration = u'\u0420\u0415\u0413\u0418\u0421\u0422\u0420\u0410\u0426\u0418\u042f'
vote = u'\u0413\u041b\u0410\u0421\u0423\u0412\u0410\u041d\u0415'

parties_count = 6

def parse_excel_by_name(filename):
    """
    Parse excel files with vote statistics by representative.

    Assumptions
    ===========

    The .xls file starts with two lines we don't care about. All remaining lines
    contain the following fields, from left to right:
        - representative name
        - two fields we skip
        - representative's party
        - undefined number of fields containing stuff about how the
        representative voted.

    Returns
    =======

    The result is a
        dictionary:
            key: a namedtuple containing the name and party of the representative
            value: a tuple containing the vote statistics for this representative

    """
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)
    cols = sheet.ncols
    rows = sheet.nrows
    init_row = 2
    result = {}
    for row in range(init_row, rows):
        name = sheet.cell_value(rowx=row, colx=0).strip().upper()
        party = sheet.cell_value(rowx=row, colx=3).strip().upper()
        key = rep(name=name, party=party)
        value = []
        for col in range(4, cols):
            value.append(sheet.cell_value(rowx=row, colx=col))
        result[key] = tuple(value)

    return result

def parse_excel_by_party(filename):
    u"""
    Parse excel files with vote statistics by party.

    Assumptions
    ===========

    - There is a total of six parties (see parties_count above)
    - For each session, there is a line containing either "GLASUVANE" or
    "REGISTRACIA", and that's how we know what's going on
    - After this line, there are two lines we don't care about, and the next
    parties_count consecutive lines contain the vote/presence statistics by party.

    Returns
    =======

    The result is a
        dictionary:
            key: namedtuple describing the session type and additional details
            value:
                dictionary:
                    key: party
                    value:
                        dictionary:
                            key: present/expected for 'REGISTRACIA', or
                                 for/against/skipped/total for 'GLASUVANE'
                            value: corresponding numbers in int format

    """
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)
    cols = sheet.ncols
    rows = sheet.nrows
    result = {}
    row = 0
    while row < rows:
        first = sheet.cell_value(rowx=row, colx=0)
        if first.find(registration) != -1:
            kind = registration
            details = first
            key = session(kind=kind, details=details)
            row += 2
            value = {}
            for i in range(parties_count):
                row += 1
                party = sheet.cell_value(rowx=row, colx=0).strip().upper()
                present = int(sheet.cell_value(rowx=row, colx=1))
                expected = int(sheet.cell_value(rowx=row, colx=2))
                value[party] = {'present': present, 'expected': expected}
            result[key] = value
        if first.find(vote) != -1:
            kind = vote
            details = first
            key = session(kind=kind, details=details)
            row += 2
            value = {}
            for i in range(parties_count):
                row += 1
                party = sheet.cell_value(rowx=row, colx=0).strip().upper()
                voted_for = int(sheet.cell_value(rowx=row, colx=1))
                voted_against = int(sheet.cell_value(rowx=row, colx=2))
                skipped = int(sheet.cell_value(rowx=row, colx=3))
                total = int(sheet.cell_value(rowx=row, colx=4))
                value[party] = {'for': voted_for, 'against': voted_against, 'skipped': skipped, 'total': total}
            result[key] = value
        row += 1
    return result

def pprint_result_by_party(result):
    """
    Print the output of the parser for results by party.

    So that it makes more sense what it's doing.
    """
    for key in result.keys():
        print key.kind
        print key.details
        value = result[key]
        for key in value.keys():
            print key, ':', value[key]
