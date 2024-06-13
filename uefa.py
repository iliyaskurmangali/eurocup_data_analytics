import numpy as np
import pandas as pd

df=pd.read_csv('Uefa Euro Cup All Matches.csv')


def determine_winner(row):
    if row['HomeTeamGoals'] > row['AwayTeamGoals']:
        return "home_win"
    elif row['HomeTeamGoals'] < row['AwayTeamGoals']:
        return "away_win"
    else:
        return "draw"

# Apply determine_winner function to create MatchResult column
df['MatchResult'] = df.apply(determine_winner, axis=1)

def team_statistics(df, team1, team2):
    # Filter matches where team1 or team2 is either HomeTeamName or AwayTeamName
    team1_home = df[df['HomeTeamName'].str.contains(team1) | df['AwayTeamName'].str.contains(team1)]
    team2_home = df[df['HomeTeamName'].str.contains(team2) | df['AwayTeamName'].str.contains(team2)]

    # Calculate number of matches played between team1 and team2
    team1_vs_team2 = team1_home[(team1_home['HomeTeamName'].str.contains(team1) & team1_home['AwayTeamName'].str.contains(team2)) |
                                (team1_home['AwayTeamName'].str.contains(team1) & team1_home['HomeTeamName'].str.contains(team2))]

    # Calculate number of matches where team2 played against team1
    team2_vs_team1 = team2_home[(team2_home['HomeTeamName'].str.contains(team2) & team2_home['AwayTeamName'].str.contains(team1)) |
                                (team2_home['AwayTeamName'].str.contains(team2) & team2_home['HomeTeamName'].str.contains(team1))]

    total_matches = len(team1_vs_team2)

    team1_wins = len(team1_vs_team2.loc[((team1_vs_team2['HomeTeamName'].str.contains(team1)) & (team1_vs_team2['MatchResult'].str.contains('home_win'))) |
                                       ((team1_vs_team2['AwayTeamName'].str.contains(team1)) & (team1_vs_team2['MatchResult'].str.contains('away_win')))])

    team2_wins = len(team1_vs_team2.loc[((team1_vs_team2['HomeTeamName'].str.contains(team2)) & (team1_vs_team2['MatchResult'].str.contains('home_win'))) |
                                       ((team1_vs_team2['AwayTeamName'].str.contains(team2)) & (team1_vs_team2['MatchResult'].str.contains('away_win')))])

    # Calculate total goals scored by team1 and team2
    team1_goals = team1_vs_team2.loc[team1_vs_team2['HomeTeamName'].str.contains(team1), 'HomeTeamGoals'].sum() + \
                  team1_vs_team2.loc[team1_vs_team2['AwayTeamName'].str.contains(team1), 'AwayTeamGoals'].sum()

    team2_goals = team1_vs_team2.loc[team1_vs_team2['HomeTeamName'].str.contains(team2), 'HomeTeamGoals'].sum() + \
                  team1_vs_team2.loc[team1_vs_team2['AwayTeamName'].str.contains(team2), 'AwayTeamGoals'].sum()

    return total_matches, team1_wins, team2_wins, team1_goals, team2_goals

# Define the teams for which you want to calculate statistics
team1 = 'Czechoslovakia'
team2 = 'Soviet Union'

# Calculate statistics for team1 vs team2
total_matches, team1_wins, team2_wins, team1_goals, team2_goals = team_statistics(df, team1, team2)

# Print the results
print(f"Total matches between {team1} and {team2}: {total_matches}")
print(f"{team1} wins: {team1_wins}")
print(f"{team2} wins: {team2_wins}")
print(f"Total goals scored by {team1}: {team1_goals}")
print(f"Total goals scored by {team2}: {team2_goals}")
