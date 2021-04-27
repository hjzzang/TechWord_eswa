import pandas as pd
import time
import numpy as np
start = time.time()

os.chdir('D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet')
NP = pd.read_excel('190710_NP.xlsx', keep_default_na=False, encoding='cp949')
SAO = pd.read_excel('190704_10분_SAO.xlsx', keep_default_na=False, encoding='cp949')

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

end = time.time()
print(end - start)

# 64.20525646209717

SAO['s_extended'] = np.array(S_extended)
SAO['o_extended'] = np.array(O_extended)

SAO.to_excel('190710_SAO_extended.xlsx')