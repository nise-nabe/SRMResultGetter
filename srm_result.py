#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import os
import time

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

roundListUrl = 'http://www.topcoder.com/tc?module=BasicData&c=dd_round_list'
cacheFile = os.sep.join([os.environ['HOME'], '.topcoder', 'dd_round_list.xml'])

# -f つけたら強制的に取得してくる実装にしたい
if not os.path.exists(cacheFile) or time.time() - os.stat(cacheFile).st_mtime > 7 * 24 * 60 * 60:
	f = urllib2.urlopen(roundListUrl)
	cfile = open(cacheFile, 'w')
	cfile.write(f.read())
	cfile.close()

f = open(cacheFile, 'r')

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

# print roundDataUrl

roundDataUrl = 'http://www.topcoder.com/tc?module=BasicData&c=dd_round_results&rd='+roundId 
roundResultFilename = 'dd_round_result.' + roundId + '.xml'
cacheFile = os.sep.join([os.environ['HOME'], '.topcoder', roundResultFilename])

if not os.path.exists(cacheFile):
	f = urllib2.urlopen(roundDataUrl)
	cfile = open(cacheFile, 'w')
	cfile.write(f.read())
	cfile.close()

f = open(cacheFile, 'r')
dom = parseString(f.read())

for row in dom.getElementsByTagName('row'):
	handle = getData(row, 'handle')
	if handle == name:
		print roundName,
		print ox(getData(row, 'level_one_status')),
		print ox(getData(row, 'level_two_status')),
		print ox(getData(row, 'level_three_status')),
		print getData(row, 'challenge_points'),'=',
		print getData(row, 'final_points'),'pts',
		print getData(row,'old_rating'),
		print '->',
		print getData(row, 'new_rating'),
		print 
		sys.exit(0)
