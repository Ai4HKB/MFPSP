# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:40:49 2020

@author: Administer
"""
def result_prediction(species, type, output_file):
    import numpy as np
    import pandas as pd
    import os
    import sys
    import joblib
    
    
    
    results_id_proba_site=[]
    
    pred_proba=[]
    x_test=pd.read_csv('./features/allfeatures.csv',sep=',',header=0,index_col=0)
    seq_id=list(x_test.index)
    x_test=x_test.to_numpy()
    results_id_proba_site.append(seq_id)
    
    model=joblib.load("./model/"+str(species)+"/"+str(type)+"/"+str(species)+"_"+str(type)+"_100.m")
    y_pred=model.predict_proba(x_test)[:,1]
    pd.DataFrame(y_pred).to_csv("./proba_s.csv",sep=",")
    results_id_proba_site.append(y_pred)
    
    
    pred_class=list(map(lambda x: "phosphorylation_"+str(type)+"_site" if x>0.5 else "none_phosphorylation_site",y_pred))
    results_id_proba_site.append(pred_class)
    pd.DataFrame(np.array(results_id_proba_site).T,columns=["sequence_id","predicted_probability","result"]).to_csv('./results/'+output_file+".csv")
    