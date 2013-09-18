#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2

from xml.dom.minidom import parseString

def ox(resultText):
	return u'○' if resultText == 'Passed System Test' else u'×'

def getData(row, tagName, text=''):
	cnode = row.getElementsByTagName(tagName)[0].childNodes
	return cnode[0].data if len(cnode) > 0 else text

argv = sys.argv
argc = len(argv)

if argc < 2:
	print 'usage: python %s handle [srmNumber]' % argv[0]
	quit()

name = argv[1]
srm = argv[2] if argc > 2 else ''

# print name

f = urllib2.urlopen("http://www.topcoder.com/tc?module=BasicData&c=dd_round_list")
dom = parseString(f.read())
roundId = ''
roundName = ''
if srm == '':
	row = dom.getElementsByTagName('row')[-1]
	roundId = getData(row, 'round_id')
	roundName = getData(row, 'short_name')
else:
	for row in dom.getElementsByTagName('row'):
		roundName = getData(row, 'short_name')
		if srm in roundName:
			roundId = getData(row, 'round_id')
			break

if roundId == '':
	print 'invalid srm number'
	quit()

roundDataUrl = 'http://www.topcoder.com/tc?module=BasicData&c=dd_round_results&rd='+roundId 

# print roundDataUrl

f = urllib2.urlopen(roundDataUrl)
dom = parseString(f.read())

for row in dom.getElementsByTagName('row'):
	handle = getData(row, 'handle')
	if handle == name:
		print name, roundName
		print ox(getData(row, 'level_one_status')),
		print ox(getData(row, 'level_two_status')),
		print ox(getData(row, 'level_three_status')),
		print getData(row, 'challenge_points'),'=',
		print getData(row, 'final_points'),'pts',
		print 
		print getData(row,'old_rating'),
		print '->',
		print getData(row, 'new_rating'),
		print 
		break
