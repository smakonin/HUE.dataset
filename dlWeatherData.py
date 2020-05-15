#! /usr/bin/env python3
#
# dlWeatherData.py -- Copyright (C) 2020 Stephen Makonin
#

import sys, urllib.request


print()
print('Download Envirment Canada Weather Data -- v1.0 (May 14, 2020)')
print()

if len(sys.argv) < 4:
    print()
    print('USAGE: %s [Weather Station] [year] [output location]' % (sys.argv[0]))
    print()
    print('Weather Stations used: YVR, WYJ')
    print('Year example: 2016, if "flush" then data is removed except for the header')
    print('Output location example: ./final')
    print()
    print()
    exit(1)


stations = {
    'YVR': [{'id': 889, 'last day': '2013-06-12'}, {'id': 51442, 'first day': '2013-06-13'}],
    'WYJ': [{'id': 6812, 'first day': '1994-02-01'}]}

hourly_data_url = 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=%d&Year=%d&Month=%d&Day=14&timeframe=1&submit=Download+Data'

colums_wanted = [
    [4, 'date', 's', '%.10s'],
    [8, 'hour', 'd+1', '%02d'],
    [9, 'temperature', 'f', '%.1f'],
    [13, 'humidity', 'd', '%d'],
    [21, 'pressure', 'f', '%.2f'],
    [27, 'weather', 's', '%s']]
# "Longitude (x)",0
# "Latitude (y)",1
# "Station Name",2
# "Climate ID",3
# "Date/Time",4
# "Year",5
# "Month",6
# "Day",7
# "Time",8
# "Temp (°C)",9
# "Temp Flag",10
# "Dew Point Temp (°C)",11
# "Dew Point Temp Flag",12
# "Rel Hum (%)",13
# "Rel Hum Flag",14
# "Wind Dir (10s deg)",15
# "Wind Dir Flag",16
# "Wind Spd (km/h)",17
# "Wind Spd Flag",18
# "Visibility (km)",19
# "Visibility Flag",20
# "Stn Press (kPa)",21
# "Stn Press Flag",22
# "Hmdx",23
# "Hmdx Flag",24
# "Wind Chill",25
# "Wind Chill Flag",26
# "Weather",27

station_name = sys.argv[1]
year = sys.argv[2]
location = sys.argv[3]

filename = '%s/Weather_%s.csv' % (location, station_name)

if year == 'flush':
    f = open(filename, 'w')
    f.write(','.join([col[1] for col in colums_wanted]) + '\n')
    f.close()
    print('File %s is flushed.' % filename)
    print()
    exit(0)

year = int(year)
f = open(filename, 'a')
for month in range(1, 13):

    print('Downloading %s weather data for %04d-%02d...' % (station_name, year, month))

    station_ids = []
    target_stations = []

    for station in stations[station_name]:
        if 'last day' in station and int('%04d%02d' % (year, month)) <= int(station['last day'][:-3].replace('-','')) and len(station_ids) < 3:
            station_ids.append(station['id'])
            target_stations.append(station)
        elif 'first day' in station and int('%04d%02d' % (year, month)) >= int(station['first day'][:-3].replace('-','')) and len(station_ids) < 3:
            station_ids.append(station['id'])
            target_stations.append(station)
    print('\tUsing station ids:', station_ids)

    for station in target_stations:
        station_id = station['id']
        with urllib.request.urlopen(hourly_data_url % (station_id, year, month)) as response:
            data = response.read()
            csv = data.decode('utf-8')
            csv = csv.replace('"', '')

            header = True
            for row in csv.split('\r\n'):

                if header or row == '':
                    header = False
                    continue

                row = row.split(',')
                if len(row) < 1 or len(row) == 9: continue # len 9 means time change!
                line = ''

                date = colums_wanted[0][3] % row[colums_wanted[0][0]]
                if 'last day' in station and int(date.replace('-','')) > int(station['last day'].replace('-','')):
                    print('\tSwitching station id for date', date)
                    break;
                if 'first day' in station and int(date.replace('-','')) < int(station['first day'].replace('-','')):
                    continue;

                for col in colums_wanted:
                    value = None
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
                f.write(line[:-1] + '\n')

f.close()

print()
print('done!')
print()
