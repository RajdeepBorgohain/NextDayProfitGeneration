import pickle
import numpy as np
import xgboost
# from xgboost import XGBClassifier
# import xgboost as xgb

"""Input: NULL
   Output: Model
"""
def load_model():
    load_model = pickle.load(open('model/xgb_f_beta_model.sav','rb'))
    
    return load_model


""" Input: Model, Selected_date Data
    Output: Predicted Score
"""
def prediction(model,data):
    pred = model.predict_proba(data)
    score = np.average(pred[:,1:])
    
    return score