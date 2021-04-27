
import os
import pandas as pd
import re
import json

import nltk
#nltk.download('wordnet')

phrase_data = pd.read_excel('20190816_3_NP_re_df.xlsx',  keep_default_na=False)
sao_data = pd.read_excel('190715_SAO_extended.xlsx',  keep_default_na=False)

single_df = pd.DataFrame()
single_df['word'] = phrase_data['Head']
single_df['pos'] = 'n'
single_df=single_df.drop_duplicates()
single_df = single_df.reset_index(drop=True)

dep_df = pd. DataFrame()

dep_df['word'] = pd.concat([phrase_data['D1'], phrase_data['D2'],phrase_data['D3']])
dep_df['pos'] = 'n'
dep_df=dep_df.drop_duplicates().reset_index(drop=True)

so_df = pd. DataFrame()
so_df['word'] = pd.concat([sao_data['s'], sao_data['o']])
so_df['pos'] = 'n'
so_df = so_df[so_df['word']!=""]
so_df = so_df.drop_duplicates().reset_index(drop=True)

a_df = pd. DataFrame()
a_df['word'] = sao_data['a']
a_df['pos'] = 'v'
a_df = a_df[a_df['word']!=""]
a_df = a_df.drop_duplicates().reset_index(drop=True)

phrase_df = pd.concat([single_df,dep_df,so_df,a_df])
phrase_df = phrase_df[(phrase_df.pos == 'n')|(phrase_df.pos == 'v')]
#phrase_df = phrase_df[(phrase_df.word != r'[0-9]+')]
phrase_df = phrase_df[phrase_df['word'].str.contains(r'\D', na=False)]
phrase_df = phrase_df.drop_duplicates(["word"])
phrase_df = phrase_df.reset_index(drop = True)
########################################################################################################################################


import pandas as pd
from nltk.corpus import wordnet as wn

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# volcabulary 별 synset list 저장
word_list = phrase_df.word.tolist()
pos_list = phrase_df.pos.tolist()

lemma_list = []
lemma_pos_list = []
for i in range(len(word_list)):
    try:
        #this_lemma = lemmatizer.lemmatize(word_list[i], pos= pos_list[i])
        this_lemma = lemmatizer.lemmatize(word_list[i])
        if this_lemma not in lemma_list:
            lemma_list.append(this_lemma)
            lemma_pos_list.append(this_lemma+'_'+pos_list[i])
    except:
        print(word_list[i])




syn_list = []
for this_word in lemma_list:
    try:
        globals()['synset_{}'.format(this_word)] = []
        for synset in wn.synsets(this_word):

            this_synset = synset.name()
            this_synset_pos = synset.pos()
            this_word_index = list(phrase_df.word).index(this_word)
            this_word_pos = phrase_df.pos.iloc[this_word_index]

            if this_synset_pos == this_word_pos:
                globals()['synset_{}'.format(this_word)].append(this_synset)
                syn_list.append(this_synset)
                syn_list.sort()
    except:
        print(this_word)

print('^^')
# 단어별 synset bool list 만들기

syn_uniq_list = list(set(syn_list))

for this_word in lemma_list:

    this_word_syn = globals()['synset_{}'.format(this_word)]
    globals()['bool_{}'.format(this_word)] = []
    for synset in syn_uniq_list:
        try:
            syn_index = this_word_syn.index(synset)
            if syn_index >= 0:
                globals()['bool_{}'.format(this_word)].append(1)
        except:
            globals()['bool_{}'.format(this_word)].append(0)

# index는 word, column은 synset으로 데이터프레임 만들기


df = pd.DataFrame()
df = pd.DataFrame(columns= syn_uniq_list, index= lemma_list)

for this_word in lemma_list:
    df.loc[this_word] = globals()['bool_{}'.format(this_word)]

df.to_json("200128_wordnet_matching.json", orient='table')

#split_df = df.iloc[:10000,:10000]
#split_df.to_excel('word-synset.xlsx')

"""
# 이것저것

def json_table(json_dir):
    with open(json_dir, 'r') as f:   
        json_obj = json.loads(f.read())
        df = pd.DataFrame(json_obj['data']).set_index('index')
        df.index.name = None
    return df

voc_df = json_table('200123_wordnet_matching.json')

columns_name = list(df.columns)
rows_name = list(df.index.values)

split_synset = [columns_name[i].split('.') for i in range(len(columns_name))]

word_synset = [split_synset[i][0] for i in range (len(columns_name))]
pos_synset = [split_synset[i][1] for i in range (len(columns_name))]
number_synset = [split_synset[i][2] for i in range (len(columns_name))]

word_pos_number = pd.DataFrame({"word":word_synset, "pos":pos_synset, "number":number_synset})
word_pos_number.to_excel("word_pos_number.xlsx")

"""