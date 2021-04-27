#능동형만

import json
import pandas as pd

import os
global adress, adress_phrase, data

def json_open(json_dir):
    with open(json_dir) as json_data:
        obj = json.load(json_data)
        df = pd.DataFrame(obj, columns=["SENTENCENO", "WORD_NO", "RAW", "LEMMA", "CTAG", "TAG", "REL","HEAD_id", "HEAD_lemma", "HEAD_raw", "HEAD_pos"])
    return df


####################

json_dir = adress
phrase_info_dir = adress
phrase_relation_dir = adress
file_header = '_parsed_info.json'
phrase_info_file_header = '_phrase_info.json'
phrase_relation_file_header = '_phrase_relation.json'


###############

id=[]
PAT_NO = []
SENT = []
S = []
S_id = []
A = []
A_id = []
O = []
O_id = []
TYPE = []


#range(len(data))
for i in range(len(data)):
        print(i,"/",len(data))
        target_patent = data.iloc[i].번호
        file_name = str(i+1)+"_"+str(target_patent)+"_parsed_info.json"
        file_name = adress+"/"+file_name
        patent_info=json_open(file_name) # open json file of parsed dataframe for each patent

        st_in_cmp=list(set(list(patent_info.SENTENCENO))) # size for length of sentence, if len of sentence = 3, st_in_cmp = [1,2,3]
        binded_phrase_info=pd.DataFrame()
        phrase_relation_info=pd.DataFrame()

        for st_no in st_in_cmp:
            st_info = patent_info[patent_info.SENTENCENO == st_no] # extract selected sentence (st_no) from dataframe
            st_info = st_info.reset_index(drop=True) # reset index from 0 of dataframe (ex 48-74 -> 0-26)
            head_word_no_list=list(set(list(st_info.HEAD_id)))
            head_word_no_list=[int(no) for no in head_word_no_list] # extract numerical number for head word
            head_word_no_list.sort()


            nmod_word_no_list = list(set(list(st_info[st_info.REL == "nmod"].WORD_NO)))
            nmod_word_no_list = [int(no) for no in nmod_word_no_list]
            nmod_word_no_list.sort()

            nsubjpass_word_no_list = list(set(list(st_info[st_info.REL == "nsubjpass"].WORD_NO)))
            nsubjpass_word_no_list = [int(no) for no in  nsubjpass_word_no_list]
            nsubjpass_word_no_list.sort()


            s = ""
            a = ""
            o = ""

            s_id = ""
            a_id =""
            o_id = ""

            # active
            for head_word_no in head_word_no_list:
                head_word_no = str(head_word_no)
                type = "a"

                phrase_sources = st_info[st_info.HEAD_id == head_word_no]

                sa_raw = phrase_sources[(phrase_sources.REL == 'nsubj') & (phrase_sources.CTAG != 'WDT')]
                ao_raw = phrase_sources[(phrase_sources.REL == 'dobj') & (phrase_sources.CTAG != 'WDT')]


                if len(sa_raw)*len(ao_raw) > 0 :
                    s = sa_raw.LEMMA.iloc[0]
                    s_id = sa_raw.WORD_NO.iloc[0]
                    o = ao_raw.LEMMA.iloc[0]
                    o_id = ao_raw.WORD_NO.iloc[0]
                    a = list(set([sa_raw.HEAD_lemma.iloc[0]] + [ao_raw.HEAD_lemma.iloc[0]]))[0]
                    a_id = list(set([sa_raw.HEAD_id.iloc[0]] + [ao_raw.HEAD_id.iloc[0]]))[0]
                else:
                    s= ""
                    s_id = ""
                    a = ""
                    a_id = ""
                    o = ""
                    o_id = ""

                if (len(a)*len(s)>0) | (len(a)*len(o)>0) :
                    S.append(s)
                    S_id.append(s_id)
                    A.append(a)
                    A_id.append(a_id)
                    O.append(o)
                    O_id.append(o_id)
                    id.append(i+1)
                    PAT_NO.append(target_patent)
                    SENT.append(st_no)
                    TYPE.append(type)


            # passive 1 - acl+nmod+case(by) ex. 'data captured by camera'
            for nmod_word_no in nmod_word_no_list:
                type = "s1"
                nmod_word_no = str(nmod_word_no)

                # (nmod의 head 명사 중 case : by - 명사) phrase extraction - RAW:'by', HEAD:s를 나타내는 명사 / HEAD --> s
                s_raw = st_info[(st_info['HEAD_id'] == nmod_word_no) & (st_info['LEMMA'] == 'by') & (st_info['HEAD_pos'] != 'WDT')]


                if len(s_raw)>0:
                    s = s_raw.HEAD_raw.iloc[0]
                    s_id = nmod_word_no # nmod

                    ao_raw = st_info[st_info['WORD_NO'] == st_info[(st_info['WORD_NO'] == nmod_word_no)].HEAD_id.iloc[0]]
                    a = ao_raw.LEMMA.iloc[0]
                    a_id = ao_raw.WORD_NO.iloc[0]
                    if ao_raw.HEAD_pos.iloc[0] != "WDT":
                        o = ao_raw.HEAD_lemma.iloc[0]
                        o_id = ao_raw.HEAD_id.iloc[0]
                    else:
                        o = ""
                else:
                    s = ""
                    a = ""
                    o = ""

                if (len(a)*len(s)>0) | (len(a)*len(o)>0) :
                    S.append(s)
                    S_id.append(s_id)
                    A.append(a)
                    A_id.append(a_id)
                    O.append(o)
                    O_id.append(o_id)
                    id.append(i + 1)
                    PAT_NO.append(target_patent)
                    SENT.append(st_no)
                    TYPE.append(type)

            # passive 2
            for nsubjpass_no in nsubjpass_word_no_list:
                type = 's2'
                nsubjpass_no = str(nsubjpass_no)
                sa_raw = st_info[(st_info['WORD_NO'] == nsubjpass_no)]
                s = ""
                s_id = ""
                o = sa_raw.LEMMA.iloc[0]
                o_id = sa_raw.WORD_NO.iloc[0]
                a = sa_raw.HEAD_lemma.iloc[0]
                a_id = sa_raw.HEAD_id.iloc[0]

                if (len(a) * len(o)>0) :
                    S.append(s)
                    S_id.append(s_id)
                    A.append(a)
                    A_id.append(a_id)
                    O.append(o)
                    O_id.append(o_id)
                    id.append(i + 1)
                    PAT_NO.append(target_patent)
                    SENT.append(st_no)
                    TYPE.append(type)


        SAO_info_df = pd.DataFrame({"id":id ,'patent_id':PAT_NO,"sent_id": SENT,"s_id": S_id, "s": S, "a_id": A_id, "a": A, "o_id":O_id, "o":O, "type" : TYPE})


SAO_info_df.to_excel('SAO.xlsx')