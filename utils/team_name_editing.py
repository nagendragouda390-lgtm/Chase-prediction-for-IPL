# importing neccessary modules
import pandas as pd

# Reading deliveries and matches csv's
deliv = pd.read_csv("/storage/8006-15FE/IPL dataset/deliveries.csv")
match = pd.read_csv("/storage/8006-15FE/IPL dataset/matches.csv")

cols = ['id', 'season', 'city', 'date', 'match_type', 'player_of_match', 'venue', 'team1', 'team2', 'toss_winner', 'toss_decision', 'winner', 'result', 'result_margin', 'target_runs', 'target_overs', 'super_over', 'method', 'umpire1', 'umpire2']

print(f"Data before team cleaning: \n\n  deliveries : {deliv.shape}\n  matches    : {match.shape}\n")

# Changing venue name
match["city"] = match["city"].rename({"Banglore":"Bengaluru"})
# Droping old teams of IPL
def dropping_teams(df,col):
    df = df[df[col]!="Deccan Chargers"]
    df = df[df[col]!="Pune Warriors"]
    df = df[df[col]!="Gujarat Lions"]
    df = df[df[col]!="Rising Pune Supergiant"]
    df = df[df[col]!="Rising Pune Supergiants"]
    df = df[df[col]!="Kochi Tuskers Kerala"]
    
    return df

deliv = dropping_teams(deliv,"batting_team")
deliv = dropping_teams(deliv,"bowling_team")
match = dropping_teams(match,"team1")
match = dropping_teams(match,"team2")
match = dropping_teams(match,"toss_winner")
match = dropping_teams(match,"winner")

# Coverting team names to their short forms
team_names = {
    "Mumbai Indians":"MI",
    "Kolkata Knight Riders":"KKR",
    "Chennai Super Kings":"CSK",
    "Royal Challengers Bangalore":"RCB",
    "Rajasthan Royals":"RR",
    "Kings XI Punjab":"PBKS",
    "Sunrisers Hyderabad":"SRH",
    "Delhi Daredevils":"DC",
    "Delhi Capitals":"DC",
    "Punjab Kings":"PBKS",
    "Gujarat Titans":"GT",
    "Lucknow Super Giants":"LSG",
    "Royal Challengers Bengaluru":"RCB"
}

deliv["batting_team"] = deliv["batting_team"].map(team_names)
deliv["bowling_team"] = deliv["bowling_team"].map(team_names)
match["team1"] = match["team1"].map(team_names)
match["team2"] = match["team2"].map(team_names)
match["toss_winner"] = match["toss_winner"].map(team_names)
match["winner"] = match["winner"].map(team_names)

print(f"Data after team cleaning: \n\n  deliveries : {deliv.shape}\n  matches    : {match.shape}\n")

# Output: Cleaned data 
deliv.to_csv("/storage/8006-15FE/IPL dataset/cleaned_teams_ball_by_ball.csv",index=False)
match.to_csv("/storage/8006-15FE/IPL dataset/cleaned_teams_matches.csv",index=False)

