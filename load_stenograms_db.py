from stenograms_to_db import *
import shelve

stenograms_dump = shelve.open('data/stenograms_dump')
stenograms = stenograms_dump['stenograms']
print stenograms.keys()
