# -*- coding: utf-8 -*-

from Bio import SeqIO 

dict_kmer={
           "asper_s":7,
           "crypto_s":7,
           "fusari_s":7,    "fusari_t":6,
           "magna_s":7,     "magna_t":7,
           "neuro_s":7,     "neuro_t":7,
           "schizo_s":7,    "schizo_t":6,
           "sacch_s":7,     "sacch_t":7,    "sacch_y":9
          }



dict_w={
        "asper_s":1,
        "crypto_s":2,
        "fusari_s":1,   "fusari_t":7,
        "magna_s":1,    "magna_t":3,
        "neuro_s":2,    "neuro_t":1,
        "schizo_s":1,   "schizo_t":4,
        "sacch_s":1,    "sacch_t":1,    "sacch_y":1
        }


def kmer_seq(sequence, k):
    list_seq=list(sequence)
    return (list("".join(list_seq[i:i+k]) for i in range(len(sequence)-k+1)))


def w2v_kmer_corpus(input_file,k):
    with open('./sequence/w2v_kmer.txt',"w") as fil1:
        for seq_record in SeqIO.parse('./sequence/'+str(input_file), "fasta"):
            seq_id=seq_record.id
            seq=seq_record.seq
            sub_list=kmer_seq(seq,k)
            fil1.write(str(seq_id)+",")
            fil1.writelines(str(x)+"," for x in sub_list)
            fil1.write("\n")


def word_vector_flaten(sequences,word_length,vector_length, model):
    import numpy as np
    import pandas as pd
    word_features=np.zeros((len(sequences), word_length*vector_length))
    modelwv=model.wv
    for i in range(len(sequences)):    
        array=np.array([model.wv[w] if w in modelwv else np.zero(20) for w in sequences[i]])
        #print(array.shape)
        
        S= pd.Series(array.flatten())
        word_features[i]=S.values
    return word_features

def fasttext(species, type, inputfile):
    import pandas as pd
    import numpy as np
    import logging
    from gensim import utils
    import gensim
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
    
    kmer=dict_kmer[str(species)+'_'+str(type)]
    window=dict_w[str(species)+'_'+str(type)]
    w2v_kmer_corpus(inputfile,kmer)
    
    with utils.open('./sequence/w2v_kmer.txt','r',encoding='utf-8-sig') as infile:
            its_list=list(infile)
                
    list_seq=[] # 保存 kmer序列
    for x in range(len(its_list)): 
        list_seq.append(its_list[x].split(",")[1:-1])

    from gensim.models.word2vec import Word2Vec
    model = Word2Vec.load('./model/'+str(species)+'/'+str(type)+'/'+str(str(species)+'_'+str(type))+'_k'+str(kmer)+"w"+str(window)+"_shffule.model")
    X=word_vector_flaten(np.array(list_seq),41-kmer+1,20, model)
    pd.DataFrame(X).to_csv("./features/fasttext.csv", sep=",")
    
def fasttext_features(species, type, inputfile):
    encodings=fasttext(species, type, inputfile)
    
    
    
    
    
    
    