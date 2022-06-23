import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('season.sqlite')
cur = conn.cursor()

year1 = input('Enter beginning of the period:')
year2 = input('Enter ending of the period:')
round = input('Enter round:')
seasons = list()
for year in range(int(year1), int(year2), 1):
    season = str(year) + '-' + str(year+1)
    seasons.append(season)

season_id_lst = list()
for item in seasons:
    sqlstr = '''SELECT id, name FROM Season WHERE name = ? ORDER BY id
    '''
    cur.execute(sqlstr, (item, ))
    result = cur.fetchall()
    season_id_lst.append(result[0][0])

avg_num_of_points = list()
avg_gap_between_champ_leader = list()
avg_gap_between_champ_second_place = list()
avg_goals_scored = list()
avg_goals_conceded = list()
avg_goal_diff = list()

for season_id in season_id_lst:
    sqlstr1 = '''SELECT a.home_team AS team_name, a.Win+b.Win AS Wins, a.Draw+b.Draw AS Draws, a.Loss+b.Loss AS Losses,
    a.GS+b.GS AS GS, a.GC+b.GC AS GC, (a.GS+b.GS)-(a.GC+b.GC) AS GD, (a.AvgGD+b.AvgGD)/2 AS AvgGD,
    a.Points+b.Points AS Points
    FROM(
    SELECT DISTINCT t.name AS home_team, s.name, SUM(CASE
                                         WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '3'
										 WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '0'
										 WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
										 END) AS Points,
    SUM(CASE
         WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Win,
    SUM(CASE
         WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Loss,
    SUM(CASE
         WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Draw,
    SUM(substr(m.result,1,1)) AS GS, SUM(substr(m.result,-1,1)) AS GC,
    AVG(substr(m.result,1,1)-substr(m.result,-1,1)) AS AvgGD
    FROM Match m JOIN Team t
    ON t.id = home_team_id
    JOIN Season s
    ON s.id = m.season_id
    WHERE season_id = ?
    GROUP BY t.name
    ORDER BY Points DESC) AS a
    JOIN(SELECT DISTINCT t.name AS guest_team, s.name, SUM(CASE
                                         WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '3'
										 WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '0'
										 WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
										 END) AS Points,
    SUM(CASE
         WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Win,
    SUM(CASE
         WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Loss,
    SUM(CASE
         WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Draw,
    SUM(substr(m.result,-1,1)) AS GS, SUM(substr(m.result,1,1)) AS GC,
    AVG(substr(m.result,-1,1)-substr(m.result,1,1)) AS AvgGD
    FROM Match m JOIN Team t
    ON t.id = guest_team_id
    JOIN Season s
    ON s.id = m.season_id
    WHERE season_id = ?
    GROUP BY t.name
    ORDER BY Points DESC) AS b
    ON a.home_team=b.guest_team
    GROUP BY team_name
    ORDER BY Points DESC'''

    cur.execute(sqlstr1, (season_id, season_id, ))
    result = cur.fetchall()

    champion = result[0][0]


    sqlstr2 = '''SELECT a.home_team AS team_name, a.Win+b.Win AS Wins, a.Draw+b.Draw AS Draws, a.Loss+b.Loss AS Losses,
    a.GS+b.GS AS GS, a.GC+b.GC AS GC, (a.GS+b.GS)-(a.GC+b.GC) AS GD, (a.AvgGD+b.AvgGD)/2 AS AvgGD,
    a.Points+b.Points AS Points
    FROM(
    SELECT DISTINCT t.name AS home_team, s.name, SUM(CASE
                                         WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '3'
										 WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '0'
										 WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
										 END) AS Points,
    SUM(CASE
         WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Win,
    SUM(CASE
         WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Loss,
    SUM(CASE
         WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Draw,
    SUM(substr(m.result,1,1)) AS GS, SUM(substr(m.result,-1,1)) AS GC,
    AVG(substr(m.result,1,1)-substr(m.result,-1,1)) AS AvgGD, m.round_id
    FROM Match m JOIN Team t
    ON t.id = home_team_id
    JOIN Season s
    ON s.id = m.season_id
    WHERE season_id = ? AND m.round_id <= ?
    GROUP BY t.name
    ORDER BY Points DESC) AS a
    JOIN(SELECT DISTINCT t.name AS guest_team, s.name, SUM(CASE
                                         WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '3'
										 WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '0'
										 WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
										 END) AS Points,
    SUM(CASE
         WHEN substr(m.result,1,1) < substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Win,
    SUM(CASE
         WHEN substr(m.result,1,1) > substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Loss,
    SUM(CASE
         WHEN substr(m.result,1,1) = substr(m.result,-1,1) THEN '1'
		 ELSE 0
		 END) AS Draw,
    SUM(substr(m.result,-1,1)) AS GS, SUM(substr(m.result,1,1)) AS GC,
    AVG(substr(m.result,-1,1)-substr(m.result,1,1)) AS AvgGD, m.round_id
    FROM Match m JOIN Team t
    ON t.id = guest_team_id
    JOIN Season s
    ON s.id = m.season_id
    WHERE season_id = ? AND m.round_id <= ?
    GROUP BY t.name
    ORDER BY Points DESC) AS b
    ON a.home_team=b.guest_team
    GROUP BY team_name
    ORDER BY Points DESC'''

    cur.execute(sqlstr2, (season_id, round, season_id, round, ))
    result1 = cur.fetchall()
    leader = result1[0]

    second_place = result1[1]

    for team in result1:
        if team[0] == champion:
            champ = team

        else:
            continue
    gap_between_champ_leader = int()

    if champ == leader:
        gap_between_champ_leader == 0
    else:
        gap_between_champ_leader = champ[len(champ)-1] - leader[len(leader)-1]
    avg_gap_between_champ_leader.append(gap_between_champ_leader)

    gap_between_champ_second_place = champ[len(champ)-1] - second_place[len(second_place)-1]
    avg_gap_between_champ_second_place.append(gap_between_champ_second_place)

    total_points = champ[-1]
    avg_num_of_points.append(total_points)

    goals_scored = champ[-5]
    avg_goals_scored.append(goals_scored)

    goals_conceded = champ[-4]
    avg_goals_conceded.append(goals_conceded)

    goal_diff = champ[-3]
    avg_goal_diff.append(goal_diff)

def average(lst):
    return sum(lst) / len(lst)
avg_total_points = average(avg_num_of_points)
gap_bcl = average(avg_gap_between_champ_leader)
gap_bcsp = average(avg_gap_between_champ_second_place)
goals_s = average(avg_goals_scored)
goals_c = average(avg_goals_conceded)
goals_diff = average(avg_goal_diff)

print('Average total points:', avg_total_points)
print('Average gap between champion and leader:', gap_bcl)
print('Average gap between champion and runner-up:', gap_bcsp)
print('Average goals scored:', goals_s)
print('Average goals conceded:', goals_c)
print('Average goal difference:', goals_diff)

plt.plot(seasons, avg_num_of_points, color = 'green', label = 'Points')
plt.plot(seasons, avg_gap_between_champ_leader, color = 'red', label = 'Champ/Leader gap')
plt.plot(seasons, avg_gap_between_champ_second_place, color = 'yellow', label = 'Champ/Runner-up gap')
plt.plot(seasons, avg_goals_scored, color = 'orange', label = 'Goals scored')
plt.plot(seasons, avg_goals_conceded, color = 'blue', label = 'Goals conceded')
plt.plot(seasons, avg_goal_diff, color = 'black', label = 'Goal difference')
plt.legend()
plt.title("Champion's measures after 26 game weeks")
plt.show()
