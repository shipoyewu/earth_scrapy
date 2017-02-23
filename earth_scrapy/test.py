#!/usr/bin/env python2

import urllib2
import bs4

def crawl(next_url, info):
#    try:
		n_soup = bs4.BeautifulSoup(urllib2.urlopen(next_url).read())
		journal = n_soup.findAll('table', {'class':"table7"})
		print ("journal=%s" %(journal))
#	except:
#		print ('something')

if __name__ == '__main__':
	info = {}
	next_url = 'http://www.dzdczz.com/bookmululist.aspx?qi_id=1332'
	Crawl(next_url, info)
