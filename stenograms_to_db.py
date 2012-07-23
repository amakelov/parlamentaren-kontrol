from HTMLParser import HTMLParser
from urllib2 import urlopen
from collections import namedtuple
from parse_excel import *
import shelve

class StenogramsHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_marktitle = 0
        self.in_dateclass = False
        self.data_list = []
        self.date = None

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if self.in_marktitle:
                self.in_marktitle += 1

            if ('class', 'marktitle') in attrs:
                self.in_marktitle = 1
            elif ('class', 'dateclass') in attrs:
                self.in_dateclass = True

    def handle_endtag(self, tag):
        if tag == 'div' and self.in_marktitle:
            self.in_marktitle -= 1

    def handle_data(self, data):
        if self.in_dateclass:
            self.date = data.strip() #TODO there must be a date type
            self.in_dateclass = False
        elif self.in_marktitle:
            self.data_list.append(data)


stgram = namedtuple('stgram', ['date', 'text_lines', 'by_name_votes'])


if __name__ == '__main__':
    stenograms = {}
    stenogram_IDs = open('data/IDs_plenary_stenograms').readlines()
    for ID in stenogram_IDs[:2]:
        print "At ID: ", ID
        parser = StenogramsHTMLParser()
        f = urlopen('http://www.parliament.bg/bg/plenaryst/ID/'+ID)
        parser.feed(f.read().decode('utf-8'))
        print parser.date

        by_name_temp = open('data/temp.excel', 'wb') # TODO the next 3 lines should use the datetype
        day, month, year = parser.date.split('/')
        date_string = day + month + year[2:]
        by_name_web = urlopen("http://www.parliament.bg/pub/StenD/iv%s.xls" % date_string)
        by_name_temp.write(by_name_web.read())
        by_name_temp.close()
        by_name_dict = parse_excel_by_name('data/temp.excel')

        stenograms[ID]=stgram(date=parser.date,
                              text_lines=parser.data_list,
                              by_name_votes=by_name_dict)

    stenograms_dump = shelve.open('data/stenograms_dump')
    stenograms_dump['stenograms'] = stenograms
    stenograms_dump.close()
