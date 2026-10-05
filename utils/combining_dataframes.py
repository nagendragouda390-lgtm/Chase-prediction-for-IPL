#==============================
# Importing neccessary modules
#==============================
import pandas as pd

path = "/storage/8006-15FE/IPL dataset/"

match = pd.read_csv(path + "cleaned_teams_matches.csv")
deliv = pd.read_csv(path + "cleaned_teams_ball_by_ball.csv")
match_24 = pd.read_csv(path + "cleaned_teams_matches_24.csv")
deliv_24 = pd.read_csv(path + "cleaned_teams_ball_by_ball_24.csv")

#================================
# Creating features in 2024 data
#================================
deliv_24["total_runs"] = deliv_24["runs_of_bat"] + deliv_24["extras"]
deliv_24["over"] = deliv_24["over"].astype(int)
deliv_24["ball"] = (deliv_24["over"]*10)%10
deliv_24["is_wicket"] = deliv_24["wicket_type"].notna().astype(int)
match_24["target_runs"] = match_24["first_ings_score"]+1
match_24 = match_24.rename(columns = {"match_id":"id",
                            "match_winner":"winner"
                          })
deliv_24 = deliv_24.rename(columns = {"match_no":"match_id",
                                      "innings":"inning"
                                      })

#============================
# Keeping neccessary columns
#============================ 
match = match[["id", "city", "winner", "target_runs"]]
match_24 = match_24[["id", "city", "winner", "target_runs"]]

deliv = deliv[[
    "match_id", "inning", "batting_team", "bowling_team",
    "over", "ball", "total_runs", "is_wicket"
]]
deliv_24 = deliv_24[[
    "match_id", "inning", "batting_team", "bowling_team",
    "over", "ball", "total_runs", "is_wicket"
]]

#=======================
# Connecting dataframes
#=======================
match = pd.concat([match,match_24])
deliv = pd.concat([deliv,deliv_24])

df = deliv.merge(match, left_on="match_id", right_on="id").drop(columns="id")

df = df[[
    "match_id", "city", "inning", "batting_team", "bowling_team",
    "winner", "target_runs", "over", "ball", "total_runs", "is_wicket"
]]

#===========================
# Uploading final dataframe 
#===========================
df.to_csv(path + "combined_data.csv", index=False)
print("Data combined successfully.")


