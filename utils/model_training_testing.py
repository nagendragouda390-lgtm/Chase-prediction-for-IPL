#------------------------------
# importing neccessary modules
#------------------------------
import pandas as pd

from sklearn.model_selection import GroupShuffleSplit
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, QuantileTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
                             classification_report,
                             accuracy_score,
                             confusion_matrix,
                             )
import joblib
                              
#------------------
# reading csv file
#------------------
print("loading data...")
path = "/storage/8006-15FE/IPL dataset/"

df = pd.read_csv(path+"final_data.csv")

#-----------------------------
# creating feature and target
#-----------------------------
print("\ncreating features and target...")
X = df.drop(["match_id","chase"],axis=1)
y = df["chase"]

#----------------------------------------------
# classifying columns of X to cat and num cols
#----------------------------------------------
print("\nclassifying columns to catogorical and numerical...")
cat = [col for col in X.columns if X[col].dtypes == "str"]
num = [col for col in X.columns if col not in cat]

#--------------------------------------
# splitting data according to match_id
#--------------------------------------
print("\nsplitting data for training and testing...")
gss = GroupShuffleSplit(test_size=0.2,random_state=46)

train_idx, test_idx = next(gss.split(X,y,groups=df["match_id"]))

X_train,X_test = X.iloc[train_idx],X.iloc[test_idx]
y_train,y_test = y.iloc[train_idx],y.iloc[test_idx]

#-------------------------------------------
# creating preprocessing steps and pipeline
#-------------------------------------------
print("\ncreating pipeline...")
pre = ColumnTransformer([
    ("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),cat),
    ("num",QuantileTransformer(),num)
])

pipe = Pipeline([
    ("pre",pre),
    ("model",LogisticRegression())
])

#---------------------------------------
# training pipeline using training data
#---------------------------------------
print("\ntraining pipeline...")
pipe.fit(X_train,y_train)

#----------------------------
# predicting using test data
#----------------------------
print("\npredicting for test data...")
y_pred = pipe.predict(X_test)

#---------------------
# Evaluation of model
#---------------------
print("\nevaluating model...\n")
cr = classification_report(y_test,y_pred)
ac = accuracy_score(y_test,y_pred)
cm = confusion_matrix(y_test,y_pred)

print(f"Model evaluation : \n")
print(f"Acuuracy : {round(ac,2)*100}%")
print(f"\nConfusion matix :\n{cm}")
print(f"\nclassification report : \n{cr}\n")

#------------------
# Dumping pipeline
#------------------

joblib.dump(pipe,path+"chase_predictor.pkl")

print(f"model dumped succesfully to directory -> {path}chase_predictor.pkl\n")