#!usr/bin/env python

'''
Scrapes rainfall data from
http://www.imd.gov.in/section/hydro/distrainfall/districtrain.html
'''

import sys
import urllib
import urlparse
import csv
from lxml import etree

def get(url):
    '''Retrives a URL'''
    sys.stderr.write(url + '\n')
    return urllib.urlopen(url).read()

def safe(line):
    '''Strips out all unsafe / non-ASCII characters'''
    return ''.join(char for char in line if 32 <= ord(char) < 128)

# The output will be written to a CSV file with these fields
# You could output to JSON too, if you wish
out = csv.writer(sys.stdout, lineterminator='\n')
out.writerow(('state', 'district', 'year',
    'jan-rf', 'jan-dep',
    'feb-rf', 'feb-dep',
    'mar-rf', 'mar-dep',
    'apr-rf', 'apr-dep',
    'may-rf', 'may-dep',
    'jun-rf', 'jun-dep',
    'jul-rf', 'jul-dep',
    'aug-rf', 'aug-dep',
    'sep-rf', 'sep-dep',
    'oct-rf', 'oct-dep',
    'nov-rf', 'dec-dep',
    'dec-rf', 'dec-dep',
    ))

# Download the main URL
url = 'http://www.imd.gov.in/section/hydro/distrainfall/districtrain.html'
tree = etree.HTML(get(url))

# The states are listed as <li><a href="...">State name</a></li>
# We loop through those...
for state in tree.findall('.//li/a'):
    state_url = urlparse.urljoin(url, state.get('href'))
    tree2 = etree.HTML(get(state_url))

    # The districts are listed as <li><a href="...">District name</a></li>
    # We loop through those
    for district in tree2.findall('.//li/a'):
        district_url = urlparse.urljoin(state_url, district.get('href'))
        text = get(district_url)

        # Process each line in the text
        for line in text.split('\n'):
            # Find the column boundaries
            if line.find('R/F %DEP.') >= 0:
                pos = [0, 4]
                for i, char in enumerate(line):
                    if ord(char) <= 32 and i > 0 and ord(line[i-1]) > 32:
                        pos.append(i)

            # Process only the lines that start with a year: 2006, 2007, etc.
            line = safe(line.strip())
            if not line.startswith('20'): continue
            values = [line[pos[i]:pos[i+1]].strip() for i, p in enumerate(pos[:-1])]
            out.writerow([safe(state.text),safe(district.text)]+values)

