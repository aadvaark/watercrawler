
import urllib2, urllib
from BeautifulSoup import BeautifulSoup
import md5
import os

def wget(url, cache=True):
    if cache:
         path = "cache/" + md5.md5(url).hexdigest()
         if os.path.exists(path):
             return open(path).read()
         else:
             #print "downloading", url
             #print "saving to", path
             html = urllib2.urlopen(url).read()
             with open(path, "w") as f:
                 f.write(html)
    else:
        #print "downloading", url
        html = urllib2.urlopen(url).read()
    return html

def get_soup(html):
    return BeautifulSoup(html)
    
def parse_data(url):
    html = wget(url)
    soup = get_soup(html)
    
    table = soup.findAll("table")[1]
    
    values = [tr.findAll("td")[-1].getText() for tr in table.findAll("tr")]
    
    print "\t".join(values)

    """
    for tr in table.findAll("tr"):
        values = [td.getText() for td in tr.findAll(["th", "td"])]
    """

def main():
    url = "http://cgwb.gov.in/SR/cgwbindex.htm"
    
    html = wget(url)
    soup = get_soup(html)
    
    links = [urllib.basejoin(url, a['href']) for a in soup.findAll("area")]
            
    for link in links:
        parse_data(link)

if __name__ == '__main__':
    main()