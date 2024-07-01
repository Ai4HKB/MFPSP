# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:40:49 2020

@author: Administer
"""

feature_list1=['AAC.csv', 'CTDC.csv', 'PAAC_2.csv', 'QSOrder_1.csv', 'EAAC_5.csv', 'BINARY.csv']

feature_list2=['AAC.csv', 'CTDC.csv', 'PAAC_2.csv', 'QSOrder_1.csv', 'EAAC_5.csv']



def feature_merge(species, type):
    import numpy as np
    import pandas as pd
    
    ## physicochemical feature merge
    species_type=str(species)+"_"+str(type) 
    if species_type in ["sacch_s","sacch_t","magna_s","neuro_s","schizo_s","fusari_s","crypto_s"]:
        feature_list=feature_list1
    else:
        feature_list=feature_list2
      
    df1=pd.read_csv("./model/"+str(species)+"/"+str(type)+"/"+str(species_type)+".csv")
    n=0
    nn=0
    for fea in feature_list:
        print(fea)
        n=n+1
        if n==1:           
            dfx=pd.read_csv('./features/'+str(fea),sep=',',header=None,index_col=0).iloc[:,0:] 
            print((dfx.shape[1]))
        else:
            if fea in ["BINARY.csv","EAAC_5.csv"]:
                sele=df1[fea.split(".csv")[0]].to_numpy()
                sele=sele[~np.isnan(sele)]
                dfn=pd.read_csv('./features/'+str(fea),sep=',',header=None,index_col=0).iloc[:,sele]
                
            else:
                dfn=pd.read_csv('./features/'+str(fea),sep=',',header=None,index_col=0).iloc[:,0:]
            
            dfx=pd.concat([dfx,dfn],axis=1)
            print((dfn.shape[1]))
           
    sele2=df1["allphy"].to_numpy()
    sele2=sele2[~np.isnan(sele2)]
    pd.DataFrame(dfx).iloc[:,sele2].to_csv("./features/physicochemical.csv",sep=",")
    
    # physicochemical feature scale
    import joblib
    dfx=pd.read_csv('./features/physicochemical.csv',sep=',',index_col=0,header=0)
    dfx_ind=dfx.index
    min_max_scaler = joblib.load('./model/'+str(species)+'/'+str(type)+'/'+str(species_type)+'_scaler.gz')
    s = min_max_scaler.transform(dfx)
    pd.DataFrame(s,index=dfx_ind).to_csv('./features/physicochemical_features.csv',sep=',',)


def feature_merge_physi_kmer(species,type):
    import pandas as pd, numpy as np
    
    species_type=str(species)+"_"+str(type)
    df1=pd.read_csv("./model/"+str(species)+"/"+str(type)+"/"+str(species_type)+".csv")
    sele1=df1['kmer']
    sele1=sele1[~np.isnan(sele1)]

    dfn=pd.read_csv('./features/fasttext.csv',sep=',',header=0,index_col=0).iloc[:,sele1]    
    dfx=pd.read_csv('./features/physicochemical_features.csv',sep=',',header=0,index_col=0)
    dfx_ind=dfx.index
    dfx=pd.concat([pd.DataFrame(dfx.to_numpy()),dfn],axis=1)
    
    pd.DataFrame(dfx).to_csv('./features/111111.csv',sep=",") 
    
    sele2=df1['allga']
    sele2=sele2[~np.isnan(sele2)]
        
    dfx=dfx.iloc[:,sele2]

    pd.DataFrame(dfx).to_csv('./features/allfeatures.csv',sep=",")     
            
            
            
def feature_sele(type):
    import pandas as pd
    if type=="s":
        sele_length=178
    elif type=="t":
        sele_length=146
    else:
        sele_length=188
    
    X=pd.read_csv('./features/combined_features.csv',sep=',',index_col=0,header=0)
    
    feature_ranking=pd.read_csv('./model/lgbclf_feature_importances_by_gain_sort_'+str(type)+'.csv',sep=",",header=None,index_col=None).to_numpy()[:,0]
    sele_list=[]
    for i in range(sele_length):
        sele_list.append(int(feature_ranking[i]))
        X_sele=X.iloc[:,sele_list]

    X_sele.to_csv("./features/sele_combined_features.csv",sep=",")

def feature_scaler(type):
    import joblib
    import pandas as pd
    
    dfx=pd.read_csv('./features/sele_combined_features.csv',sep=',',index_col=0,header=0)
    dfx_ind=dfx.index
    min_max_scaler = joblib.load('./model/'+str(type)+'_scaler.gz')
    s = min_max_scaler.transform(dfx)
    pd.DataFrame(s,index=dfx_ind).to_csv('./features/mm_sele_combined_features.csv',sep=',',)