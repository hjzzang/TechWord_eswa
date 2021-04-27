import os
import pandas as pd
import json
import multiprocessing
from nltk.tokenize import sent_tokenize
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.stem import WordNetLemmatizer

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


#############################
def json_open(json_dir):
    with open(json_dir) as json_data:
        obj = json.load(json_data)
        df = pd.DataFrame(obj, columns=["SENTENCENO", "WORD_NO", "RAW", "LEMMA", "CTAG", "TAG", "FEATS", "HEAD", "REL"])
    return df


####################

json_dir = adress
phrase_info_dir = adress
phrase_relation_dir = adress
file_header = '_parsed_info.json'
phrase_info_file_header = '_phrase_info.json'
phrase_relation_file_header = '_phrase_relation.json'


# range(len(data))
for i in range(5):
    try:
        print(i, "/", len(data))
        target_patent = data.iloc[i].번호
        file_name = str(i + 1) + "_" + str(target_patent) + "_parsed_info.json"
        file_name = adress + "/" + file_name
        patent_info = json_open(file_name)  # open json file of parsed dataframe for each patent

        st_in_cmp = list(set(list(patent_info.SENTENCENO)))  # size for length of sentence, if len of sentence = 3, st_in_cmp = [1,2,3]
        binded_phrase_info = pd.DataFrame()
        phrase_relation_info = pd.DataFrame()

        for st_no in st_in_cmp:
            st_info = patent_info[patent_info.SENTENCENO == st_no]  # extract selected sentence (st_no) from dataframe
            st_info = st_info.reset_index(drop=True)  # reset index from 0 of dataframe (ex 48-74 -> 0-26)

            st_info = (st_info.TAG == "NN" | st_info.TAG == "NNS"  )



            head_word_no_list = list(set(list(st_info.HEAD)))
            head_word_no_list = [int(no) for no in head_word_no_list]  # extract numerical number for head word
            head_word_no_list.sort()

            top_word_no_list = []
            top_word_list = []
            phrase_sources_no_list = []
            phrase_raw_list = []
            phrase_lemma_list = []
            phrase_partial_list = []
            phrase_noun_JJ_list = []

            for head_word_no in head_word_no_list:
                head_word_no = str(head_word_no)
                phrase_sources = st_info[st_info.HEAD == head_word_no]
                phrase_sources = st_info[ (st_info.REL == 'amod')| (st_info.REL == 'compound')]

                if head_word_no == '0':  # except for root word
                    pass

                else:
                    top_word_no_list.append(head_word_no)
                    top_word_df = st_info[st_info.WORD_NO == head_word_no]
                    top_word_list.append(top_word_df.iloc[0].LEMMA)

                    phrase_sources_no_list.append(
                        ", ".join(list(phrase_sources.WORD_NO)))  # make list which has same head
                    head_word_info = st_info[st_info.WORD_NO == head_word_no]
                    phrase_sources_all = head_word_info.append(phrase_sources, ignore_index=True)
                    phrase_sources_all["WORD_NO"] = [int(word_no) for word_no in
                                                     list(phrase_sources_all.WORD_NO)]  # ???
                    phrase_sources_all = phrase_sources_all.sort_values(by="WORD_NO", ascending=True)

                    this_phrase_raw_all = list(phrase_sources_all.RAW)
                    phrase_raw_list.append(" ".join(this_phrase_raw_all))  # make list phrase as raw ver.

                    this_phrase_lemma_all = list(phrase_sources_all.LEMMA)
                    phrase_lemma_list.append(" ".join(this_phrase_lemma_all))  # make list phrase as lemma ver.

                    this_phrase_target_only_df = phrase_sources_all[
                        phrase_sources_all["TAG"].str.contains("NN") | phrase_sources_all["TAG"].str.contains("RB") |
                        phrase_sources_all["TAG"].str.contains("IN") | phrase_sources_all["TAG"].str.contains("JJ") |
                        phrase_sources_all["TAG"].str.contains("JJ") | phrase_sources_all["TAG"].str.contains("PDT") |
                        phrase_sources_all["TAG"].str.contains("VB") |
                        phrase_sources_all["LEMMA"].str.match("not") | phrase_sources_all["LEMMA"].str.match(
                            "neither") |
                        phrase_sources_all["LEMMA"].str.match("fail") | phrase_sources_all["LEMMA"].str.match(
                            "failure") |
                        phrase_sources_all["LEMMA"].str.match("non") | phrase_sources_all["LEMMA"].str.match("none") |
                        phrase_sources_all["LEMMA"].str.match("without") | phrase_sources_all["LEMMA"].str.match("no")]
                    this_phrase_target_only = list(this_phrase_target_only_df.LEMMA)
                    phrase_partial_list.append(" ".join(this_phrase_target_only))

                    this_phrase_noun_JJ_only_df = phrase_sources_all[
                        phrase_sources_all["TAG"].str.contains("NN") | phrase_sources_all["TAG"].str.contains("JJ")]
                    this_phrase_noun_JJ_only = list(this_phrase_noun_JJ_only_df.LEMMA)
                    phrase_noun_JJ_list.append(" ".join(this_phrase_noun_JJ_only))
                    # Phrase 정보만 저장

                    phrase_info_df = pd.DataFrame(
                        {"Top_Word_NO": top_word_no_list, "Top_Word": top_word_list, "Sources": phrase_sources_no_list,
                         "Raw_phrase": phrase_raw_list, "Lemma_phrase": phrase_lemma_list,
                         "Partial_phrase": phrase_partial_list, "Noun_JJ_phrase": phrase_noun_JJ_list})

                    phrase_info_df["Phrase_No"] = [i for i in range(1, len(phrase_info_df) + 1)]
                    phrase_info_df["Sentence_No"] = st_no
                    phrase_file_name = "%s/%s_%s_%s_phrased_info.json" % (adress_phrase, i + 1, target_patent, st_no)

                    phrase_info_df.to_json(phrase_file_name, orient='records')
    except:
                i = i + 1