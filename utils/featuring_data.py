#------------------------------
# importing neccessary modules
#------------------------------
import pandas as pd
import numpy as np

#-------------------
# reading dataframe
#-------------------
path = "/storage/8006-15FE/IPL dataset/"

df = pd.read_csv(path+"combined_data.csv")

#--------------------------------
# Wether chasing team won or not
#--------------------------------
df["chase"] = (df["batting_team"]==df["winner"]).astype(int)

#-----------------------------
# keeping second innings only
#-----------------------------
df = df[df["inning"]==2]

#------------------
# current score
#------------------ 
df["current_runs"] = df.groupby(["match_id","inning"])["total_runs"].cumsum()

#--------------------
# current wickets
#--------------------
df["current_wickets"] = df.groupby(["match_id","inning"])["is_wicket"].cumsum()

#--------------
# current balls
#--------------
df["current_balls"] = df["over"]*6 + df["ball"]

#-----------------
# current runrate
#-----------------
df["crr"] = np.where(df["current_balls"]>0,
                     df["current_runs"]*6/df["current_balls"],
                     0)

#-----------------
# Runs per wicket
#-----------------
df["rpw"] = np.where(
                    df["current_wickets"]>0,
                    df["current_runs"]/df["current_wickets"],
                    df["current_runs"])

#--------------
# required runs
#--------------
df["required_runs"] = np.where(
                            df["target_runs"]>df["current_runs"],
                            df["target_runs"]-df["current_runs"],
                            0)

#-----------
# Balls left
#-----------
df["balls_left"] = np.where(
                            df["current_balls"]<120,
                            120 - df["current_balls"],
                            0
)

#-------------------
# required run rate
#-------------------
df["rrr"] = np.where(
                df["balls_left"]>0,
                df["required_runs"]*6/df["balls_left"],
                0)

#--------------
# wickets left
#--------------
df["wickets_left"] = 10 - df["current_wickets"]

#---------------------------
# required runs per wickets
#---------------------------
df["rrpw"] = np.where(
                df["wickets_left"]>0,
                df["required_runs"]/df["wickets_left"],
                0)

#----------
# pressure
#----------
df["pressure"] = np.where(df["crr"]>0,
                df["rrr"]/df["crr"],
                0)

#---------------------------------
# keeping neccessary columns only
#---------------------------------
df = df[[
            "match_id",
            "city",
            "batting_team",
            "bowling_team",
            "target_runs",
            "current_runs",
            "current_balls",
            "current_wickets",
            "crr",
            "rpw",
            "required_runs",
            "balls_left",
            "wickets_left",
            "rrr",
            "rrpw",
            "pressure",
            "chase"
]]

#--------------------------
# uploding final dataframe
#--------------------------
df.to_csv(path+"final_data.csv",index=False)


