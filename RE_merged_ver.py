import os
import pandas as pd
import json
import nltk
import multiprocessing
from datetime import date, time, datetime
from nltk.tokenize import sent_tokenize
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import time
"""
ready!
"""

# setting work directory and name of folder ver.
root_dir = 'D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet'
root_dir = 'C:\\Users\\hyejin\\Dropbox\\bithong\\lab_ver\\1.techwordnet'
os.chdir(root_dir)

ver = '201209_'
adress = ver + 'parsing'
# os.mkdir( adress + "/")

# raw patnet data (defalt file of wisdomain ver.)
# data = pd.read_csv('data_B60_2018.csv', header=4, keep_default_na=False, encoding='cp949')

data1 = pd.read_csv('0_CSV1907113442.csv', header=4, keep_default_na=False)
data2 = pd.read_csv('2_CSV1907112026.csv', header=4, keep_default_na=False)
data3 = pd.read_csv('3_CSV1907112555.csv', header=4, keep_default_na=False)
data4 = pd.read_csv('4_CSV1907113147.csv', header=4, keep_default_na=False)

data = pd.concat([data1, data2, data3, data4], ignore_index= True)

data = pd.read_excel('data_final.xlsx', keep_default_na=False,encoding='UTF-8')



"""
1. parsed_information
"""

###################
start1 = datetime.now()
print(start1)

# preprocessing patent into sent_tokenize and parsing
lemmatizer = WordNetLemmatizer()


# range(len(data))
for i in range(len(data)):
    if i%100 == 0: print(str(i),"/",str(len(data)))
    sent_id = []
    word_id = []
    raw = []
    lemma = []
    ctag = []
    tag = []
    head_id = []
    rel = []
    head_raw = []
    head_lemma = []
    head_pos = []
    json_by_patent = pd.DataFrame()
    patent_no = data.iloc[i].번호
    data_abs = data.요약.iloc[i]
    #print(i, "/", len(data))
    for j in range(len(sent_tokenize(data_abs))):
        data_abs_sent = sent_tokenize(data_abs)[j]
        dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
        parse, = dep_parser.raw_parse(data_abs_sent)
        txt = str(parse.to_conll(10))
        txt_split = txt.split('\n')
        for txt in txt_split:
            word_info = txt.split('\t')
            if (len(word_info)) == 10:
                sent_id.append(j + 1)
                word_id.append(word_info[0])
                raw.append(word_info[1])
                ctag.append(word_info[3])
                tag.append(word_info[4])
                head_id.append(word_info[6])
                rel.append(word_info[7])
                try:
                    lemma.append(lemmatizer.lemmatize(word_info[1].lower(),word_info[4][0].lower())) # 명사/형용사로 쓰이는 동사의 lemma 처리
                except:
                    lemma.append(word_info[2])
        for k in head_id[len(head_raw):]:
            try:
                head_raw.append(raw[int(k)-1+n])
                head_lemma.append(lemma[int(k)-1+n])
                head_pos.append(tag[int(k)-1+n])
            except:
                head_raw.append(raw[int(k)-1])
                head_lemma.append(lemma[int(k)-1])
                head_pos.append(tag[int(k)-1])

        n = len(head_raw)

    dependency_test = pd.DataFrame(
        {"SENTENCENO": sent_id, "WORD_NO": word_id, "RAW": raw, "LEMMA": lemma, "CTAG": ctag, "TAG": tag,
          "HEAD_id": head_id, "HEAD_lemma": head_lemma, "HEAD_raw": head_raw, "HEAD_pos": head_pos, "REL": rel})
    file_name = "%s/%s_%s_parsed_info.json" % (adress, i + 1, patent_no)
    json_by_patent = json_by_patent.append(dependency_test, ignore_index=True)
    json_by_patent.to_json(file_name, orient='records')

end1 = datetime.now()
print(end1)
print('1:', end1 - start1)

#######################"""
#문장단위




#######################
def json_open(json_dir):
    with open(json_dir) as json_data:
        obj = json.load(json_data)
        df = pd.DataFrame(obj, columns=["SENTENCENO", "WORD_NO", "RAW", "LEMMA", "CTAG", "TAG", "REL","HEAD_id", "HEAD_lemma", "HEAD_raw", "HEAD_pos"])
    return df



"""
2. NP
"""
start2 = datetime.now()
print(start2)

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
    # print(i, "/", len(data))
    target_patent = data.iloc[i].번호
    file_name = str(i + 1) + "_" + str(target_patent) + "_parsed_info.json"
    file_name = adress + "/" + file_name
    patent_info = json_open(file_name)  # open json file of parsed dataframe for each patent

    for j in range(len(patent_info)):
        phrase_info_dir = adress
        #NP
        if (patent_info.HEAD_pos.iloc[j][0] == 'N' and (
                patent_info.REL[j] == 'amod' or patent_info.REL[j] == 'compound') and patent_info.HEAD_id[j] > \
            patent_info.WORD_NO[j]) or patent_info.TAG.iloc[j][0] == 'N':

            json_dir = adress
            phrase = phrase + " " + patent_info.LEMMA[j]
            pos_phrase = pos_phrase + " " + patent_info.TAG[j][0]
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

ANP_info_df = pd.DataFrame({"id":id,'patent_id':PAT_NO,"sent_id": SENT, "type":TYPE,"word_id":WORD_ID,"phrase":PHRASE, "POS":POS, "head":HEAD, "HEAD_id":HEAD_id, "CNT":CNT,"REL":REL})



ANP_info_df.to_excel( ver + 'ANP.xlsx')
time.sleep(10)

end2 = datetime.now()
print(end2)
print('2:', end2 - start2)


"""
2-1 only Noun!
"""

start2_1 = datetime.now()
print(start2_1)

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

l = WordNetLemmatizer()

# range(len(data))
for i in range(len(data)):
    # print(i, "/", len(data))
    target_patent = data.iloc[i].번호
    file_name = str(i + 1) + "_" + str(target_patent) + "_parsed_info.json"
    file_name = adress + "/" + file_name
    patent_info = json_open(file_name)  # open json file of parsed dataframe for each patent

    for j in range(len(patent_info)):
        phrase_info_dir = adress
        #NP
        if (patent_info.HEAD_pos.iloc[j][0] == 'N' and (
                patent_info.REL[j] == patent_info.REL[j] == 'compound') and patent_info.HEAD_id[j] > \
            patent_info.WORD_NO[j]) or patent_info.TAG.iloc[j][0] == 'N':

            json_dir = adress

            phrase = phrase + " " + patent_info.LEMMA[j]
            pos_phrase = pos_phrase + " " + patent_info.TAG[j][0]

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



NP_info_df.to_excel( ver + 'NP.xlsx')
time.sleep(10)
end2_1 = datetime.now()
print(end2_1)
print('2:', end2_1 - start2_1)


"""
3. NP_reorganizing
"""
start3 = datetime.now()
print(start3)

NP = pd.read_excel(ver + 'NP.xlsx', keep_default_na = False, encoding='cp949')

#data = pd.read_csv('data_B60_2018.csv', header=4, keep_default_na=False, encoding='cp949')[0:100]

ID = []
PATENT_ID =[]
SENT_ID=[]
HEAD_ID = []
HEAD = []
HEAD_pos = []
Full = []
D1_ID = []
D1 = []
D1_pos = []
D2_ID = []
D2 = []
D2_pos = []
D3_ID = []
D3 = []
D3_pos = []
Num = []



# len(NP)
for i in range (len(NP)):

    #extract within 4 words
    if NP.CNT[i] <= 4:
        #print(i)

        id = NP.id[i]
        num = NP.CNT[i]
        patent_id = NP.patent_id[i]
        sent_id = NP.sent_id[i]
        word_id_list = NP.word_id[i].split()
        word_list = str(NP.phrase[i]).split()
        pos_list = NP.POS[i].split()


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

        full = d3 + " " + d2 + " " + d1 + " " + head_word
        full = full.strip()

        ID.append(id)
        Num.append(num)
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
        Full.append(full)





NP_framing_df = pd.DataFrame({"ID":ID, "patent_id":PATENT_ID, "sent_id":SENT_ID,"Num":Num,  "D3": D3, "D2": D2, "D1": D1,"HEAD": HEAD, "FULL": Full, "D3_pos":D3_pos, "D2_pos":D2_pos, "D1_pos":D1_pos, "D3_id":D3_ID, "D2_id":D2_ID, "D1_id":D1_ID, "head_id":HEAD_ID})

NP_framing_df.to_excel( ver + 'NP_framing_revised_df.xlsx')
time.sleep(10)
end3 = datetime.now()
print(end3)
print('3:', end3 - start3)


"""
4. NP_hierarchy
"""
start4 = datetime.now()
print(start4)



# RE_3_NP_reorganizing


NP_framing_df = pd.read_excel('190715_NP_framing_revised_df.xlsx', keep_default_na = False)
ty_df = NP_framing_df
#ty_df = ty_df[0:499]

head_all = list(ty_df.HEAD)
uniq_head=list(set(head_all))
#uniq_head.sort()
#uniq_head=uniq_head[0:100]
D1_binded_result=pd.DataFrame()
print('for문1')
for head in uniq_head:
    D1_list = []
    D1_count_list = []
    D1_pos_list = []
    target_D1 = ty_df[ty_df.HEAD == head]

    this_D1_cand = list(target_D1.D1)

    this_D1_uniq = list(set(this_D1_cand))
    #this_D1_uniq.sort()

    for D1 in this_D1_uniq:
        D1_df = target_D1[target_D1.D1 == D1]

        D1_list.append(D1)
        D1_count_list.append(this_D1_cand.count(D1))

        D1_df = D1_df.reset_index(drop=True)
        D1_pos_list.append(D1_df.iloc[0].D1_pos)
    D1_result=pd.DataFrame({"D1":this_D1_uniq,"Head":head, "D1_Count":D1_count_list, "D1_POS":D1_pos_list})
    D1_binded_result = D1_binded_result.append(D1_result,ignore_index=True)

D2_binded_result = pd.DataFrame()
print('for문2')
for i in range(len(D1_binded_result)):
    this_head = D1_binded_result.iloc[i].Head
    this_D1 = D1_binded_result.iloc[i].D1
    #this_D1_count = D1_binded_result.iloc[i].D1_Count
    this_D1_POS = D1_binded_result.iloc[i].D1_POS
    #전체에서 헤드만 같은것 찾기
    target_D2 = ty_df[ty_df.HEAD == this_head]
    #찾은것 중에서 D1도 같은것 찾기
    target_D2 = target_D2[target_D2.D1 == this_D1]


    #Head와 D1이 고정된 상태에서 나올 수 있는 D2의 리스트
    this_D2_list = list(target_D2.D2)
    #Head와 D1이 고정된 상태에서 D2의 uniq만 구함(전체 리스트에서 Uniq가 들어가 있는 수가 Head-D1-D2 조합의 수이기 때문에
    this_D2_uniq = list(set(this_D2_list))
    #this_D2_uniq.sort()

    #Head - D1이 고정된 상태에서 고유한 D2에 대한 정보를 저장하기 위한 리스트
    D2_list = []
    D2_count_list = []
    D2_pos_list = []
    for D2 in this_D2_uniq:
        #target_D2(Head, D1만 고정된 것에서 D2를 갖는 column만 조회함
        D2_df=target_D2[target_D2.D2 == D2]
        D2_df = D2_df.reset_index(drop=True)
        D2_list.append(D2)
        D2_count_list.append(this_D2_list.count(D2))
        D2_pos_list.append(D2_df.iloc[0].D2_pos)

        D2_result = pd.DataFrame({"D2": D2_list, "D1": this_D1, "Head": this_head, "D2_Count": D2_count_list,"D1_POS": this_D1_POS, "D2_POS": D2_pos_list})

    D2_binded_result = D2_binded_result.append(D2_result, ignore_index=True)

D3_binded_result = pd.DataFrame()
print('for문3')
# D3!!!!!!!!!!!!
for i in range(len(D2_binded_result)):
    this_head = D2_binded_result.iloc[i].Head

    this_D1 = D2_binded_result.iloc[i].D1
    this_D1_POS = D2_binded_result.iloc[i].D1_POS

    this_D2 = D2_binded_result.iloc[i].D2
    this_D2_POS = D2_binded_result.iloc[i].D2_POS


    #전체에서 헤드만 같은것 찾기
    target_D3 = ty_df[ty_df.HEAD == this_head]
    #찾은것 중에서 D1도 같은것 찾기
    target_D3 = target_D3[target_D3.D1 == this_D1]
    # 찾은것 중에서 D2도 같은것 찾기
    target_D3 = target_D3[target_D3.D2 == this_D2]


    #Head, D1, D2가 고정된 상태에서 나올 수 있는 D3의 리스트
    this_D3_list = list(target_D3.D3)
    #Head와 D1이 고정된 상태에서 D2의 uniq만 구함(전체 리스트에서 Uniq가 들어가 있는 수가 Head-D1-D2 조합의 수이기 때문에
    this_D3_uniq = list(set(this_D3_list))
    #this_D3_uniq.sort()

    #Head, D1, D2가 고정된 상태에서 고유한 D3에 대한 정보를 저장하기 위한 리스트
    D3_list = []
    D3_count_list = []
    D3_pos_list = []
    Full_dep = []
    for D3 in this_D3_uniq:
        #target_D3(Head, D1,D2가 고정된 것에서 D3를 갖는 column만 조회함
        D3_df=target_D3[target_D3.D3 == D3]
        D3_df = D3_df.reset_index(drop=True)
        D3_list.append(D3)
        D3_count_list.append(this_D3_list.count(D3))
        D3_pos_list.append(D3_df.iloc[0].D3_pos)

        full_dep = (D3_list[0] + " "+ this_D2 + " " + this_D1).strip()

        D3_result = pd.DataFrame(
            {"D3": D3_list, "D2": this_D2, "D1": this_D1, "Dep": full_dep, "Head": this_head, "Count": D3_count_list,
             "D3_POS": D3_pos_list, "D2_POS": this_D2_POS, "D1_POS": this_D1_POS})

    D3_binded_result =D3_binded_result.append(D3_result, ignore_index=True)


time.sleep(10)
"""
word="WORD"
list1=[1,2,3,4]
pd.DataFrame({"Word":word,"LIST":list1})
"""

#time record: 1334.2329425811768

D3_binded_result.to_excel(ver + "NP_hierarchy.xlsx")

data = D3_binded_result
#data = pd.read_excel('190715_NP_hierarchy.xlsx', keep_default_na = False)

Len = []
print('for문4')
for hj in range(len(data)):
    len_phrase = 0
    head = [str(i) for i in data.Head.iloc[[hj]]][0]
    d1 = [str(i) for i in data.D1.iloc[[hj]]][0]
    d2 = [str(i) for i in data.D2.iloc[[hj]]][0]
    d3 = [str(i) for i in data.D3.iloc[[hj]]][0]
    if len(head) >=1 :
        len_head = 1
    else: len_head = 0

    if len(d1) >=1 :
        len_d1 = 1
    else: len_d1 = 0

    if len(d2) >=1 :
        len_d2 = 1
    else: len_d2 = 0

    if len(d3) >=1 :
        len_d3 = 1
    else: len_d3 = 0

    len_phrase = len_head+len_d1+len_d2+len_d3
    Len.append(len_phrase)

Len_df = pd.DataFrame({"len":Len})

NP_hierarchy_reviesed = pd.concat([data, Len_df], axis = 1)

NP_hierarchy_reviesed.to_excel(ver+"NP_hierarchy_revised.xlsx")

end4 = datetime.now()
print(end4)
print('4:', end4 - start4)

"""
5. SAO , 주어동사목적어만 단일단어
"""
start5 = datetime.now()
print(start5)
#능동형만


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
        #print(i,"/",len(data))
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


SAO_info_df.to_excel(ver +'SAO.xlsx')


end5 = datetime.now()
print(end5)
print('5:', end5 - start5)
time.sleep(10)
"""
6. SAO_extended
"""
start6 = datetime.now()
print(start6)

import numpy as np


NP = pd.read_excel(ver + 'NP.xlsx', keep_default_na=False, encoding='cp949')
SAO = pd.read_excel(ver + 'SAO.xlsx', keep_default_na=False, encoding='cp949')

S_extended = []
O_extended = []

for i in range(len(SAO)):
    id = SAO.iloc[i].id
    sent_id = SAO.iloc[i].sent_id
    s_id = SAO.iloc[i].s_id
    o_id = SAO.iloc[i].o_id


    hj_NP = NP[NP.id == id]
    hj_NP = hj_NP [ hj_NP.sent_id == sent_id]

    try:
        hj_s = hj_NP[hj_NP.HEAD_id == int(s_id)]
        s_ex = hj_s.phrase.iloc[0]
    except:
        s_ex = ""

    try:
        hj_o = hj_NP[hj_NP.HEAD_id == int(o_id)]
        o_ex = hj_o.phrase.iloc[0]
    except:
        o_ex = ""

    S_extended.append(s_ex)
    O_extended.append(o_ex)



# 64.20525646209717

SAO['s_extended'] = np.array(S_extended)
SAO['o_extended'] = np.array(O_extended)

SAO.to_excel(ver + 'SAO_extended.xlsx')

end6 = datetime.now()
print(end6)
print(end6 - start6)