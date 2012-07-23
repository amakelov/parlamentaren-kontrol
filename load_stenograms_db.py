from stenograms_to_db import *
from parse_excel import *
import shelve

stenograms_dump = shelve.open('data/stenograms_dump')
stenograms = stenograms_dump['stenograms']
print stenograms.keys()
