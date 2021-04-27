import os
import pandas as pd
root_dir = 'D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet'
ver = '190712_'


adress = ver + 'parsing'

os.chdir(root_dir)


component_rule = ['contain', 'form', 'include', 'consist', 'have', 'comprise', 'compose', 'form', 'manufacture', 'obtain', 'produce', 'make']

SAO = pd.read_excel(ver + 'SAO_extended.xlsx', keep_default_na = False, encoding='cp949')

df = pd.DataFrame(columns=list(SAO.columns))

for verb in component_rule:
    com = SAO[SAO.a == verb]
    for i in range(len(com)):
        if (len(com.iloc[i].s_extended) > 0 and len(com.iloc[i].o_extended) > 0):
            df = df.append(com.iloc[i])


df = df.reset_index(drop=True)

