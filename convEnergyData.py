#! /usr/bin/env python3
#
# convEnergyData.py -- Copyright (C) 2018 Stephen Makonin
#

import sys, csv, glob

names = {'res': 'Residential', 'com': 'Commercial', 'ind': 'Industrial'}

print()
print('Convert BCHydro Export Data -- v1.0 (Jan. 28, 2018)')
print()

if len(sys.argv) != 3:
    print()
    print('USAGE: %s [type: %s] [id]' % (sys.argv[0], '|'.join(names.keys())))
    print()
    print()
    exit(1)



btype = sys.argv[1]
if btype not in names:
    print('Type not found:', btype)
    exit(1)
bid = int(sys.argv[2])
mkey = '%s-%d' % (btype, bid)


mappings = {}
fp = open('./EnergyDataMapping.tab', 'r')
reader = csv.reader(fp, delimiter='\t')
reader.__next__()
for row in reader:
    if len(row) == 0: continue
    if len(row) == 1: exit(1)
    if len(row) == 2: value = []
    if len(row) == 3: value = row[2].split(',')
    if len(row) >= 4: exit(1)
    key = '%s-%d' % (row[1].strip(), int(row[0]))
    mappings[key] = value

if mkey not in mappings:
    print('Key not found:', mkey)
    exit(1)

if mappings[mkey] == []:
    print('There is no mapped file for this key:', mkey)
    exit(1)

ofp = open('./final/%s_%d.csv' % (names[btype], bid), 'w')
ofp.write('date,hour,energy_kWh\n')
count = 0
nonnull = 0
for fid in mappings[mkey]:
    fp = open('./raw.energy/%s/%s.csv' % (btype, fid), 'r')
    reader = csv.reader(fp)
    reader.__next__()
    for row in reader:
        ts = row[2] # ex: 2015-01-30 00:00, 2/21/2015 0:00

        if '-' in ts:
            date = ts[:10]
            hour = ts[11:13]
        elif '/' in ts:
            (dt,tm) = ts.split(' ')
            dt = dt.split('/')
            tm = tm.split(':')
            date = '%04d-%02d-%02d' % (int(dt[2]), int(dt[0]), int(dt[1]))
            hour = '%02d' % (int(tm[0]))
        else:
            print('Unknown ts format:', ts)
            exit(0)

        consumption = row[3]
        if consumption == 'N/A':
            consumption = ''
        else:
            nonnull += 1
        ofp.write('%s,%s,%s\n' % (date, hour, consumption))
        count += 1
    fp.close()
ofp.close()

print('Missing data points:', count - nonnull)
print('Data coverage is %.3f' % (nonnull / count))
print('done!')
print()
