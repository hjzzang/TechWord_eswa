import os
import pandas as pd
os.chdir('D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet')

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