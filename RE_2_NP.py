import json
import pandas as pd

import os

def json_open(json_dir):
    with open(json_dir) as json_data:
        obj = json.load(json_data)
        df = pd.DataFrame(obj, columns=["SENTENCENO", "WORD_NO", "RAW", "LEMMA", "CTAG", "TAG", "REL","HEAD_id", "HEAD_lemma", "HEAD_raw", "HEAD_pos"])
    return df


####################
# define directory of parsing files
adress = 'D:/Dropbox/bithong//lab_ver/1.techwordnet/190625_parsing'

# define directory of phrase results
adress_phrase = 'D:/Dropbox/bithong//lab_ver/1.techwordnet/190625_phrase'

os.chdir('D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet')
data = pd.read_csv('data_B60_2018.csv', header=4, keep_default_na=False, encoding='cp949')

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
CNT = []
PHRASE = []
POS = []
HEAD = []
HEAD_id = []
REL = []
WORD_ID = []
TYPE = []

phrase = ""
pos_phrase = ""
rel_phrase = ""
id_set = ""
type = ""


# range(len(data))
for i in range(len(data)):
    print(i, "/", len(data))
    target_patent = data.iloc[i].번호
    file_name = str(i + 1) + "_" + str(target_patent) + "_parsed_info.json"
    file_name = adress + "/" + file_name
    patent_info = json_open(file_name)  # open json file of parsed dataframe for each patent

    for j in range(len(patent_info)):
        #NP
        if (patent_info.HEAD_pos.iloc[j][0] == 'N' and (
                patent_info.REL[j] == 'amod' or patent_info.REL[j] == 'compound') and patent_info.HEAD_id[j] > \
                patent_info.WORD_NO[j]) or patent_info.TAG.iloc[j][0] == 'N':
            phrase = phrase + " " + patent_info.RAW[j]
            pos_phrase = pos_phrase + " " + patent_info.TAG[j]
            rel_phrase = rel_phrase + " " + patent_info.REL[j]
            id_set = id_set + " " + patent_info.WORD_NO[j]
            type = "NP"

        elif len(phrase) > 0 and phrase.count(" ")-1 == id_set.count(" ")-1 == pos_phrase.count(" ")-1 == rel_phrase.count(" ")-1:
            id.append(i+1)
            PAT_NO.append(target_patent)
            SENT.append(patent_info.SENTENCENO[j])
            CNT.append(phrase.count(" "))
            PHRASE.append(phrase[1:])
            HEAD.append(phrase.split()[phrase.count(" ")-1])
            HEAD_id.append(id_set.split()[phrase.count(" ") - 1])
            POS.append(pos_phrase[1:])
            REL.append(rel_phrase[1:len(rel_phrase)])
            WORD_ID.append(id_set[1:])
            TYPE.append(type)

            phrase = ""
            pos_phrase = ""
            rel_phrase = ""
            id_set = ""
            type = ""


NP_info_df = pd.DataFrame({"id":id,'patent_id':PAT_NO,"sent_id": SENT, "type":TYPE,"word_id":WORD_ID,"phrase":PHRASE, "POS":POS, "head":HEAD, "HEAD_id":HEAD_id, "CNT":CNT,"REL":REL})




NP_info_df.to_excel('190710_NP.xlsx')





