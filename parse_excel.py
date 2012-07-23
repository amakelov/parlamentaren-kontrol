import xlrd
from collections import namedtuple

rep = namedtuple('rep', ['name', 'party'])

def parse_excel_by_name(filename):
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
