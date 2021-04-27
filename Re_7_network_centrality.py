import os
import pandas as pd
import re
import networkx as nx

#ver = '20190816'
ver = '201209'
#root_dir = 'D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet'
#os.chdir(root_dir)

phrase_data = pd.read_excel('201209_NP_hierarchy_revised.xlsx',  keep_default_na=False)

# build dataframe 'from - to' for network analysis
Head = []
Dep = []
Cnt = []

d2_word = phrase_data[phrase_data.len == 2]
d3_word = phrase_data[phrase_data.len == 3]
d4_word = phrase_data[phrase_data.len == 4]

for hj in range(len(d2_word)):
    Head.append(d2_word.Head.iloc[hj])
    Dep.append(d2_word.D1.iloc[hj])
    Cnt.append(d2_word.Count.iloc[hj])

for hj in range(len(d3_word)):
    Head.append(d3_word.Head.iloc[hj])
    Dep.append(d3_word.D1.iloc[hj])
    Cnt.append(d3_word.Count.iloc[hj])
    Head.append(d3_word.D1.iloc[hj])
    Dep.append(d3_word.D2.iloc[hj])
    Cnt.append(d3_word.Count.iloc[hj])

for hj in range(len(d4_word)):
    Head.append(d4_word.Head.iloc[hj])
    Dep.append(d4_word.D1.iloc[hj])
    Cnt.append(d3_word.Count.iloc[hj])
    Head.append(d4_word.D1.iloc[hj])
    Dep.append(d4_word.D2.iloc[hj])
    Cnt.append(d3_word.Count.iloc[hj])
    Head.append(d4_word.D2.iloc[hj])
    Dep.append(d4_word.D3.iloc[hj])
    Cnt.append(d4_word.Count.iloc[hj])

fromto_df = pd.DataFrame({'from_node':Dep, 'to_node':Head, 'cnt':Cnt})

fromto_uniq_df = fromto_df.groupby(['from_node','to_node'])['cnt'].sum().reset_index()


stopwords1_regex =('[^a-zA-Z0-9_]')
num_regex = ('[0-9]')


md_del_dep_binded_result = pd.DataFrame()

for k in range(len(fromto_uniq_df)):
    print( k , "/",  len(fromto_uniq_df))
    this_from = str(fromto_uniq_df.iloc[k].from_node)
    this_to = str(fromto_uniq_df.iloc[k].to_node)

    from_stopwords_list=re.findall(stopwords1_regex,this_from)
    from_num_list = re.findall(num_regex, this_from)

    to_stopwords_list = re.findall(stopwords1_regex, this_to)
    to_num_list = re.findall(num_regex, this_to)

    noise_bool = from_stopwords_list + from_num_list + to_stopwords_list + to_num_list
    if len(noise_bool)==0:
        md_del_dep_binded_result = md_del_dep_binded_result.append(fromto_uniq_df.iloc[k], ignore_index=True)



fromnodes = list(md_del_dep_binded_result.from_node)
tonodes = list(md_del_dep_binded_result.to_node)
weight = list(md_del_dep_binded_result.cnt)

G = nx.DiGraph()
for i in range(len(md_del_dep_binded_result)):
    #G.add_edge(fromnodes[i], tonodes[i])
    G.add_edge(fromnodes[i], tonodes[i], weight = weight[i])

Word = []
Out = []
In = []


in_degree = nx.in_degree_centrality(G)
out_degree = nx.out_degree_centrality(G)
closeness = nx.closeness_centrality(G)
betweeness = nx.betweenness_centrality(G)
edge_betw = nx.edge_betweenness_centrality(G)
pgrank = nx.pagerank(G)

o_wordlist = list(out_degree.keys())
i_wordlist = list(in_degree.keys())
c_wordlist = list(closeness.keys())
b_wordlist = list(betweeness.keys())
p_wordlist = list(pgrank.keys())
e_edgelist = list(edge_betw.keys())

dep_list = [word_pair[0] for word_pair in e_edgelist]
head_list = [word_pair[1] for word_pair in e_edgelist]

in_degree_result = list(in_degree.values())
out_degree_result = list(out_degree.values())
closeness_result = list(closeness.values())
betweeness_result = list(betweeness.values())
pgrank_result = list(pgrank.values())
edge_betw_result = list(edge_betw.values())

word_centrality_df = pd.DataFrame({'word':o_wordlist, 'in': in_degree_result, 'out': out_degree_result, 'closeness': closeness_result, 'betweeness': betweeness_result, 'pgrank':pgrank_result})
edge_centrality_df = pd.DataFrame({'dep':dep_list, 'head':head_list, 'edge_btw_cen':edge_betw_result})

word_centrality_df.to_excel(ver + 'word centrality.xlsx')
edge_centrality_df.to_excel(ver + 'edge centrality.xlsx')

#
NP_df = pd.read_excel('201209_NP_hierarchy_revised.xlsx', keep_default_na=False)
Centrality_df = pd.read_excel('201209word centrality.xlsx', keep_default_na=False)


word_list = ['Head', 'D1', 'D2', 'D3']

for word in word_list:
    Centrality_df[word] = Centrality_df['word']
    NP_df = NP_df.merge(Centrality_df[[word, 'in']], how='left')
    NP_df = NP_df.rename(columns={'in': word+"_in"})
    NP_df = NP_df.merge(Centrality_df[[word, 'out']], how='left')
    NP_df = NP_df.rename(columns={'out': word + "_out"})

NP_df = NP_df.fillna(0)

DC = []
for i in range(len(NP_df)):
    if NP_df.len.iloc[i] == 1:
        dc = NP_df.Head_in.iloc[i]
        DC.append(dc)
    elif NP_df.len.iloc[i] == 2:
        dc = NP_df.Head_in.iloc[i] * NP_df.D1_out.iloc[i]
        DC.append(dc)
    elif NP_df.len.iloc[i] == 3:
        dc = (NP_df.Head_in.iloc[i] * NP_df.D1_out.iloc[i] + NP_df.D1_in.iloc[i]* NP_df.D2_out.iloc[i]) /2
        DC.append(dc)
    elif NP_df.len.iloc[i] == 4:
        dc = (NP_df.Head_in.iloc[i] * NP_df.D1_out.iloc[i] + NP_df.D1_in.iloc[i] * NP_df.D2_out.iloc[i]+ NP_df.D3_in.iloc[i]* NP_df.D3_out.iloc[i])/3
        DC.append(dc)
    #print(dc)


NP_df['DC'] = DC
NP_re_df = NP_df[(NP_df.DC > 0) & (NP_df.Head != 'a') & (NP_df.Head_in != 0)]
NP_re_df = NP_re_df.reset_index(drop=True)

NP_re_df.to_excel('201209_NP_re_df.xlsx')

# SAO

import os
import pandas as pd
import re
import networkx as nx

#os.chdir('D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet')

NP_re_df = pd.read_excel('201209_NP_re_df.xlsx', keep_default_na=False)
SAO_df = pd.read_excel('201209_SAO_extended.xlsx', keep_default_na=False)

ver = '20200109'

# 추출한 SAO에서 앞서 도출한 NP와 매칭되는 S와 O만 남긴다/ 나머지는 stopwords / 노이즈로 간주
NP_full_list=[i+" "+j for i,j in zip(NP_re_df["Dep"], NP_re_df["Head"])]
NP_re_df["NP_full"] = NP_full_list
NP_re_df['s_extended'] = NP_re_df['NP_full']
NP_re_df['o_extended'] = NP_re_df['NP_full']


SAO_df = SAO_df.merge(NP_re_df[['s_extended', 'DC']], how='left')
SAO_df = SAO_df.rename(columns={'DC': "s_DC"})
SAO_df = SAO_df.merge(NP_re_df[['o_extended', 'DC']], how='left')
SAO_df = SAO_df.rename(columns={'DC': "o_DC"})

SAO_df = SAO_df.fillna(0)

s_re = []
o_re = []
for hj in range(len(SAO_df)):
    if SAO_df.s_extended.iloc[hj] == 0:
        s_re.append("")
    else:
        s_re.append(SAO_df.s_extended.iloc[hj])
    if SAO_df.o_extended.iloc[hj] == 0:
        o_re.append("")
    else:
        o_re.append(SAO_df.o_extended.iloc[hj])

SAO_df['s_re'] = s_re
SAO_df['o_re'] = o_re

SAO_uniq_df = SAO_df.groupby(['s_re','o_re','a']).size().to_frame('Cnt').reset_index()



# from-to 데이터 셋으로 변환

From= []
To = []
Cnt = []

for i in range(len(SAO_uniq_df)):
    From.append(SAO_uniq_df.s_re[i])
    To.append(SAO_uniq_df.a[i])
    Cnt.append(SAO_uniq_df.Cnt[i])
    From.append(SAO_uniq_df.a[i])
    To.append(SAO_uniq_df.o_re[i])
    Cnt.append(SAO_uniq_df.Cnt[i])

fromto_df = pd.DataFrame({'from_node': From, 'to_node':To, 'cnt':Cnt})
fromto_uniq_df = fromto_df.groupby(['from_node','to_node'])['cnt'].sum().reset_index()

fromto_uniq_df = fromto_uniq_df[(fromto_uniq_df.from_node != '') & (fromto_uniq_df.to_node != '')]
fromto_uniq_df = fromto_uniq_df.reset_index(drop=True)


stopwords1_regex =('[^a-zA-Z0-9_]')
num_regex = ('[0-9]')



md_del_dep_binded_result=pd.DataFrame()
for k in range(len(fromto_uniq_df)):
    print( k , "/",  len(fromto_uniq_df))
    this_from = str(fromto_uniq_df.iloc[k].from_node)
    this_to = str(fromto_uniq_df.iloc[k].to_node)

    from_stopwords_list=re.findall(stopwords1_regex,this_from)
    from_num_list = re.findall(num_regex, this_from)

    to_stopwords_list = re.findall(stopwords1_regex, this_to)
    to_num_list = re.findall(num_regex, this_to)

    noise_bool = from_stopwords_list + from_num_list + to_stopwords_list + to_num_list
    if len(noise_bool)==0:
        md_del_dep_binded_result = md_del_dep_binded_result.append(fromto_uniq_df.iloc[k], ignore_index=True)

fromnodes = list(md_del_dep_binded_result.from_node)
tonodes = list(md_del_dep_binded_result.to_node)
weight = list(md_del_dep_binded_result.cnt)

G = nx.DiGraph()
for i in range(len(md_del_dep_binded_result)):
    #G.add_edge(fromnodes[i], tonodes[i])
    G.add_edge(fromnodes[i], tonodes[i], weight = weight[i])

Word = []
Out = []
In = []


in_degree = nx.in_degree_centrality(G)
out_degree = nx.out_degree_centrality(G)
closeness = nx.closeness_centrality(G)
betweeness = nx.betweenness_centrality(G)
edge_betw = nx.edge_betweenness_centrality(G)
pgrank = nx.pagerank(G)

o_wordlist = list(out_degree.keys())
i_wordlist = list(in_degree.keys())
c_wordlist = list(closeness.keys())
b_wordlist = list(betweeness.keys())
p_wordlist = list(pgrank.keys())
e_edgelist = list(edge_betw.keys())

dep_list = [word_pair[0] for word_pair in e_edgelist]
head_list = [word_pair[1] for word_pair in e_edgelist]

in_degree_result = list(in_degree.values())
out_degree_result = list(out_degree.values())
closeness_result = list(closeness.values())
betweeness_result = list(betweeness.values())
pgrank_result = list(pgrank.values())
edge_betw_result = list(edge_betw.values())

word_centrality_df = pd.DataFrame({'word':o_wordlist, 'in': in_degree_result, 'out': out_degree_result, 'closeness': closeness_result, 'betweeness': betweeness_result, 'pgrank':pgrank_result})
edge_centrality_df = pd.DataFrame({'dep':dep_list, 'head':head_list, 'edge_btw_cen':edge_betw_result})


word_centrality_df.to_excel(ver + 'SAO_word centrality.xlsx')
edge_centrality_df.to_excel(ver + 'SAO_edge centrality.xlsx')
