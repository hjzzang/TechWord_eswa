import os
import pandas as pd
import json
import multiprocessing
from nltk.tokenize import sent_tokenize
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.stem import WordNetLemmatizer
global adress, adress_phrase, data

os.chdir('D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet')
data = pd.read_csv('data_B60_2018.csv', header=4, keep_default_na=False, encoding='cp949')

# define directory of parsing files
adress = 'D:/Dropbox/bithong//lab_ver/1.techwordnet/190625_parsing'

# define directory of phrase results
adress_phrase = 'D:/Dropbox/bithong//lab_ver/1.techwordnet/190625_phrase'


# preprocessing patent into sent_tokenize and parsing
lemmatizer = WordNetLemmatizer()


# range(len(data))
for i in range(len(data)):
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
    print(i, "/", len(data))
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




# parsed 몇갠지 셀라고

cnt = 0
sent = 0

for i in range(len(data)):
    target_patent = data.iloc[i].번호
    file_name = str(i + 1) + "_" + str(target_patent) + "_parsed_info.json"
    file_name = adress + "/" + file_name
    patent_info = json_open(file_name)  # open json file of parsed dataframe for each patent
    cnt = cnt + patent_info.shape[0]
    sent = sent + patent_info.SENTENCENO[len(patent_info)-1]


