import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Uefa Euro Cup All Matches.csv')

# Function to determine match result
def determine_winner(row):
    if row['HomeTeamGoals'] > row['AwayTeamGoals']:
        return "home_win"
    elif row['HomeTeamGoals'] < row['AwayTeamGoals']:
        return "away_win"
    else:
        return "draw"

# Apply determine_winner function to create MatchResult column
df['MatchResult'] = df.apply(determine_winner, axis=1)

# Function to calculate team statistics
def team_statistics(df, team1, team2):
    team1_home = df[df['HomeTeamName'].str.contains(team1, case=False)]
    team1_away = df[df['AwayTeamName'].str.contains(team1, case=False)]
    team2_home = df[df['HomeTeamName'].str.contains(team2, case=False)]
    team2_away = df[df['AwayTeamName'].str.contains(team2, case=False)]

    team1_matches = pd.concat([team1_home, team1_away])
    team2_matches = pd.concat([team2_home, team2_away])

    # Matches between team1 and team2
    team1_vs_team2 = team1_matches[(team1_matches['HomeTeamName'].str.contains(team1, case=False) & team1_matches['AwayTeamName'].str.contains(team2, case=False)) |
                                    (team1_matches['AwayTeamName'].str.contains(team1, case=False) & team1_matches['HomeTeamName'].str.contains(team2, case=False))]

    total_matches = len(team1_vs_team2)
    team1_wins = len(team1_vs_team2[team1_vs_team2['MatchResult'] == 'home_win'])
    team2_wins = len(team1_vs_team2[team1_vs_team2['MatchResult'] == 'away_win'])
    draws = len(team1_vs_team2[team1_vs_team2['MatchResult'] == 'draw'])

    team1_goals = team1_vs_team2['HomeTeamGoals'].sum() + team1_vs_team2['AwayTeamGoals'].sum()

    team2_goals = team1_matches.loc[team1_matches['HomeTeamName'].str.contains(team2, case=False), 'HomeTeamGoals'].sum() + \
                  team1_matches.loc[team1_matches['AwayTeamName'].str.contains(team2, case=False), 'AwayTeamGoals'].sum()

    return total_matches, team1_wins, team2_wins, draws, team1_goals, team2_goals

# Streamlit app
st.title('UEFA Euro Cup Team Statistics')


# List of teams for selection
teams = [
    'Albania', 'Austria', 'Belgium', 'Bulgaria', 'CIS', 'Croatia', 'Czech Republic', 'Czechoslovakia',
    'Denmark', 'England', 'FR Yugoslavia', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
    'Italy', 'Latvia', 'Netherlands', 'Northern Ireland', 'Norway', 'Poland', 'Portugal',
    'Republic of Ireland', 'Romania', 'Russia', 'Scotland', 'Slovakia', 'Slovenia', 'Soviet Union',
    'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'Wales', 'West Germany', 'Yugoslavia'
]


# User input for teams using selectbox
team1 = st.selectbox('Select Team 1:', teams)
team2 = st.selectbox('Select Team 2:', teams)

if st.button('Calculate Statistics'):
    total_matches, team1_wins, team2_wins, draws, team1_goals, team2_goals = team_statistics(df, team1, team2)
    st.write(f"### Statistics between {team1} and {team2}")
    st.write(f"Total matches: {total_matches}")
    st.write(f"{team1} wins: {team1_wins}")
    st.write(f"{team2} wins: {team2_wins}")
    st.write(f"Draws: {draws}")
    st.write(f"Total goals by {team1}: {team1_goals}")
    st.write(f"Total goals by {team2}: {team2_goals}")

    # Visualization: Bar chart for match results
    results = pd.DataFrame({
        'Team': [team1, team2, 'Draws'],
        'Wins': [team1_wins, team2_wins, draws]
    })
    fig, ax = plt.subplots()
    results.plot(x='Team', y='Wins', kind='bar', ax=ax, color=['blue', 'green', 'orange'])
    ax.set_title('Match Results')
    ax.set_ylabel('Number of Wins')
    st.pyplot(fig)

    # Visualization: Bar chart for goals scored
    goals = pd.DataFrame({
        'Team': [team1, team2],
        'Goals': [team1_goals, team2_goals]
    })
    fig_goals, ax_goals = plt.subplots()
    goals.plot(x='Team', y='Goals', kind='bar', ax=ax_goals, color=['blue', 'green'])
    ax_goals.set_title('Total Goals Scored')
    ax_goals.set_ylabel('Number of Goals')
    st.pyplot(fig_goals)
