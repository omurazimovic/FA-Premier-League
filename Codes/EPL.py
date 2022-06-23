import csv
import re
import sqlite3

conn = sqlite3.connect('season.sqlite')
cur = conn.cursor()

year1 = input('Enter beginning of the period:')
year2 = input('Enter ending of the period:')
seasons = list()
for year in range(int(year1), int(year2), 1):
    season = str(year) + '-' + str(year+1)
    seasons.append(season)
format = '.csv'
databases = [x + format for x in seasons]

for database in databases:
    try:
        with open(database, 'r') as myFile:
            reader = csv.reader(myFile)
            next(reader)
            season = list()
            for row in reader:
                if row[0] == '?':
                    round = row[2].rsplit(' ',1)[1]
                    round = re.sub('[(){}<>]','',round)
                    row[0] = round
                team1 = row[2].rsplit(' ',1)[0]
                row[2] = team1
                team2 = row[5].rsplit(' ',1)[0]
                row[5] = team2
                year = row[1].split(' ',5)[3]
                if year not in season:
                    season.append(year)
                if len(season) == 2:
                    sn = '-'.join([str(item) for item in season])
                else:
                    sn = season[0] + '-' + str(int(season[0])+1)
                row.append(sn)
                print(row)
                cur.execute('''INSERT OR IGNORE INTO Team (name)
                VALUES ( ? )''', ( row[2], ) )
                cur.execute('''INSERT OR IGNORE INTO Team (name)
                VALUES ( ? )''', ( row[5], ) )
                cur.execute('SELECT id FROM Team WHERE name = ? ', (row[2], ))
                home_team_id = cur.fetchone()[0]
                cur.execute('SELECT id FROM Team WHERE name = ? ', (row[5], ))
                guest_team_id = cur.fetchone()[0]

                cur.execute('''INSERT OR IGNORE INTO Season (name)
                VALUES ( ? )''', ( row[6], ) )
                cur.execute('SELECT id FROM Season WHERE name = ? ', (row[6], ))
                season_id = cur.fetchone()[0]

                cur.execute('''INSERT OR IGNORE INTO Round (name)
                VALUES ( ? )''', ( row[0], ) )
                cur.execute('SELECT id FROM Round WHERE name = ? ', (row[0], ))
                round_id = cur.fetchone()[0]

                cur.execute('''INSERT OR REPLACE INTO Match
                    (season_id, round_id, home_team_id, guest_team_id, result, date)
                    VALUES ( ?, ?, ?, ?, ?, ? )''',
                    ( season_id, round_id, home_team_id, guest_team_id, row[3], row[1] ) )
                conn.commit()
    except:
        continue
