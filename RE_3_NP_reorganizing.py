import os
import pandas as pd

global adress, adress_phrase, data

os.chdir('D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet')

NP = pd.read_excel('NP.xlsx', keep_default_na=False, encoding='cp949')

ID = []
PATENT_ID =[]
SENT_ID=[]
HEAD_ID = []
HEAD = []
HEAD_pos = []
D1_ID = []
D1 = []
D1_pos = []
D2_ID = []
D2 = []
D2_pos = []
D3_ID = []
D3 = []
D3_pos = []



# len(NP)
for i in range (len(NP)):

    #extract within 4 words
    if NP.CNT[i] <= 4:
        #print(i)

        id = NP.id[i]
        patent_id = NP.patent_id[i]
        sent_id = NP.sent_id[i]
        word_id_list = NP.ID[i].split()
        word_list = NP.NP[i].split()
        pos_list = NP.NP_POS[i].split()

        reverse_word_id_list = list(reversed(word_id_list))
        reverse_word_list = list(reversed(word_list))
        reverse_pos_list = list(reversed(pos_list))

        head_word = reverse_word_list[0]
        head_id = reverse_word_id_list[0]
        head_pos = reverse_pos_list[0]

        dep_id1 = ""
        dep_id2 = ""
        dep_id3 = ""
        dep1 = ""
        dep2 = ""
        dep3 = ""
        dep_pos1 = ""
        dep_pos2 = ""
        dep_pos3 = ""



        for j in range(1,len(word_list)):
            globals()['dep_id{}'.format(j)] = reverse_word_id_list[j]
            globals()['dep{}'.format(j)]= reverse_word_list[j]
            globals()['dep_pos{}'.format(j)] = reverse_pos_list[j]
            #print('word_list',j)

        try:
            d1_id = dep_id1
            d1 = dep1.lower()
            d1_pos = dep_pos1
            #print('d1', d1)
        except NameError:
            d1_id = ""
            d1 = ""
            d1_pos = ""
            #print('d1 ', 'error')

        try:
            d2_id = dep_id2
            d2 = dep2.lower()
            d2_pos = dep_pos2
            #print('d2', d2)
        except NameError:
            d2_id = ""
            d2 = ""
            d2_pos = ""
            #print('d2 ', 'error')

        try:
            d3_id = dep_id3
            d3 = dep3.lower()
            d3_pos = dep_pos3
            #print('d3', d3)
        except NameError:
            d3_id = ""
            d3 = ""
            d3_pos = ""
            #print('d3 ', 'error')

        ID.append(id)
        PATENT_ID.append(patent_id)
        SENT_ID.append(sent_id)
        HEAD_ID.append(head_id)
        HEAD.append(head_word)
        HEAD_pos.append(head_word)
        D1_ID.append(d1_id)
        D1.append(d1)
        D1_pos.append(d1_pos)
        D2_ID.append(d2_id)
        D2.append(d2)
        D2_pos.append(d2_pos)
        D3_ID.append(d3_id)
        D3.append(d3)
        D3_pos.append(d3_pos)


NP_framing_df = pd.DataFrame({"ID":ID, "patent_id":PATENT_ID, "sent_id":SENT_ID,  "D3": D3, "D2": D2, "D1": D1,"HEAD": HEAD, "D3_pos":D3_pos, "D2_pos":D2_pos, "D1_pos":D1_pos, "D3_id":D3_ID, "D2_id":D2_ID, "D1_id":D1_ID, "head_id":HEAD_ID})









