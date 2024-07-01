# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:40:49 2020

@author: Administer
"""

def MFPSP(species,type,input_file,output_file):
    import os,sys
    work_path=os.path.abspath('.')
    os.chdir(work_path)
    sys.path.append('./feature_scripts/')
    # print(os.getcwd())
    import AAC,CTDC,QSOrder,EAAC,PAAC,BINARY,Embedding_features
    import sequence_read_save
    import feature_combine, predict
    print("step_1: sequence checking......")
    input_file=input_file
    fastas = sequence_read_save.read_protein_sequences(input_file)
    
    print("step_2: sequence encoding......")
    
    # physicochemical features
    sequence_read_save.file_remove()
    AAC.AAC_feature(fastas)
    CTDC.CTDC_feature(fastas)
    QSOrder.QSOrder_feature(fastas,type)
    EAAC.EAAC_feature(fastas,type)
    PAAC.PAAC_feature(fastas,type)
    BINARY.BINARY_feature(fastas,type)
    
    # embedding features
    Embedding_features.fasttext_features(species, type, input_file)
    
    # feature combine
    feature_combine.feature_merge(species, type)
    feature_combine.feature_merge_physi_kmer(species, type)
    
    print("step_3: result preiction.......")
    predict.result_prediction(species,type,output_file)
    sequence_read_save.file_remove()



if __name__=='__main__':
    import argparse
    import pandas as pd
    import os
    work_path=os.path.abspath('.')
    os.chdir(work_path)
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--species_name", help="species_name",)
    parser.add_argument("-t","--phosphorylation_type", help="site type: s, y, or t",)
    parser.add_argument("-i","--inputfile", help="input fasta file",)
    parser.add_argument("-o","--outputfile", help="output fasta file",)
    args = parser.parse_args()
    species=args.species_name
    type=args.phosphorylation_type
    input_file=args.inputfile
    output_file=args.outputfile
    
    print("work launched")
    MFPSP(species, type, input_file,output_file)
    print("job finished !")
    
    
    #example python MFPSP.py -s sacch -t s -i testing.fasta -o 123.fasta