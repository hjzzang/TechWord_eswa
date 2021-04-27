import os
import pandas as pd



#os.chdir('D:\\Dropbox\\bithong\\lab_ver\\1.techwordnet')

SAO_extended_df = pd.read_excel('201209_SAO_extended.xlsx', keep_default_na=False)
SAO_Centrality_df = pd.read_excel('20200109SAO_word centrality.xlsx', keep_default_na=False)


SAO_Centrality_df['a'] = SAO_Centrality_df['word']
SAO_extended_df = SAO_extended_df.merge(SAO_Centrality_df[['a', 'in']], how='left')
SAO_extended_df = SAO_extended_df.rename(columns={'in': 'a_in'})
SAO_extended_df = SAO_extended_df.merge(SAO_Centrality_df[['a', 'out']], how='left')
SAO_extended_df = SAO_extended_df.rename(columns={'out': 'a_out'})

SAO_Centrality_df['s_extended'] = SAO_Centrality_df['word']
SAO_extended_df = SAO_extended_df.merge(SAO_Centrality_df[['s_extended', 'out']], how='left')
SAO_extended_df = SAO_extended_df.rename(columns={'out': 's_out'})

SAO_Centrality_df['o_extended'] = SAO_Centrality_df['word']
SAO_extended_df = SAO_extended_df.merge(SAO_Centrality_df[['o_extended', 'in']], how='left')
SAO_extended_df = SAO_extended_df.rename(columns={'in': 'o_in'})


#SAO_extended_df.to_excel('20190815_3_SAO_re_df.xlsx')
SAO_extended_df.to_excel('201209_SAO_re_df.xlsx')