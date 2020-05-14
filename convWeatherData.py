#! /usr/bin/env python3
#
# convWeatherData.py -- Copyright (C) 2018 Stephen Makonin
#

import sys, csv, glob


print()
print('Convert Envirment Canada Weather Data -- v1.0 (Jan. 28, 2018)')
print()

print('This utility is now deprecated. Use dlWeatherData.py instead.')
print()
exit(0)


if len(sys.argv) != 3:
    print()
    print('USAGE: %s [Weather Station] [year]' % (sys.argv[0]))
    print()
    print()
    exit(1)


base_dir = './raw.weather/'
station_id = sys.argv[1]
year = int(sys.argv[2])
prefix = '%s/%s/%d-' % (base_dir, station_id, year)
sufix = '.csv'
month_filename = prefix + '%02d' + sufix
search_filename = prefix + '*' + sufix


colums_wanted = [
    [0, 'date', 's', '%.10s'],
    [4, 'hour', 'd+1', '%02d'],
    [6, 'temperature', 'f', '%.1f'],
    [10, 'humidity', 'd', '%d'],
    [18, 'pressure', 'f', '%.2f'],
    [24, 'weather', 's', '%s']]

ofp = open('./final/Weather_%s.csv' % station_id, 'a')
ofp.write(','.join([col[1] for col in colums_wanted]) + '\n')

for filename in sorted(glob.iglob(search_filename)):
    month = int(filename.replace(prefix, '').replace(sufix, ''))
    if not 0 < month < 13:
        print('ERROR: month needs to be between 1 and 12, inclusively.')
        exit(1)

    fp = open(filename, 'r')
    reader = csv.reader(fp)

    missing_row = False
    for row in reader:
        if len(row) < 1: continue
        if row[0] == 'Date/Time':
            if row[5] != 'Data Quality':
                missing_row = True
            break

    for row in reader:
        if len(row) < 1 or len(row) == 5: continue # len 6 means time change!
        line = ''
        for col in colums_wanted:
            value = None
            if missing_row and col[0] > 4:
                value = row[col[0] - 1]
            else:
                value = row[col[0]]

            if value == '':
                pass
            elif value == 'NA':
                value = ''
            elif col[2] == 's':
                value = col[3] % value
            elif col[2] == 'd+1':
                value = col[3] % (int(value[:2]) + 1)
            elif col[2] == 'd':
                value = col[3] % int(value)
            elif col[2] == 'f':
                value = col[3] % float(value)
            else:
                print('ERROR: unknown column type:', col[2])
                exit(1)
            line += value + ','
        ofp.write(line[:-1] + '\n')
    fp.close()
ofp.close()

print()
print('done!')
print()
