#--------------------------------
# importing neccessary libraries
#--------------------------------
import joblib 
import pandas as pd
import numpy as np

#---------------
# loading model
#---------------
path = "/storage/8006-15FE/IPL dataset/"

model = joblib.load(path+"chase_predictor.pkl")

#---------------------------
# taking column name needed
#---------------------------
cols = ['city', 'batting_team', 'bowling_team', 'target_runs', 'current_runs',
        'current_balls', 'current_wickets', 'crr', 'rpw', 'required_runs',
        'balls_left', 'wickets_left', 'rrr', 'rrpw', 'pressure']

#-----------------------------
# giving instructions to user
#-----------------------------
print("Instructions : ")
print("\t-Enter Q or q to quit.")
print("\t-This predictions are based on previous data.")
print("\t-It may lie.\n")

#-----------------------------
# predicting using user input
#-----------------------------
while True:
    try :
        
        #--------------
        # taking input
        #---------------
        city = input("city         : ")
        if city.lower() == "q":
            break
        bat  = input("batting_team : ")
        bow  = input("bowling_team : ")
        tar  = int(input("target       : "))
        crun = int(input("current_run  : "))
        cbal = int(input("current_ball : "))
        cwic = int(input("current_wick : "))
    
        #----------------------------------------
        # calculating other features using input
        #----------------------------------------
        crr  = crun * 6/cbal if cbal > 0 else 0
        rpw  = 0 if cwic == 0 else crun / cwic
        rrun = tar - crun
        lefb = 120 - cbal
        lefw = 10 - cwic
        rrr  = rrun * 6/lefb if lefb > 0 else 0
        rrpw = rrun / lefw if lefw > 0 else 0
        pres = 0 if crr == 0 else rrr / crr
    
        #----------------------------------
        # converting features to dataframe
        #----------------------------------
        feat = [city,bat,bow,tar,crun,cbal,cwic,crr,rpw,rrun,lefb,lefw,rrr,rrpw,pres]

        df = pd.DataFrame([feat],columns = cols)
    
        #---------------------------------------------------
        # predicting win or loss and probability of winning
        #---------------------------------------------------
        pred = model.predict(df)
        prob = model.predict_proba(df)[0][1]

        #-----------------------------
        # displaying model prediction
        #-----------------------------
        print("\nSuccessfull Chase" if pred==1 else "\nCan't chase")

        print(f"\n Win probability : {np.round(prob*100,2)}%\n")

    except Exception as e:
        print(f"Eroor : {e}")
