import pandas as pd
import time

start = time.time()
# RE_3_NP_reorganizing

ty_df = NP_framing_df
#ty_df = ty_df[0:499]

head_all = list(ty_df.HEAD)
uniq_head=list(set(head_all))
uniq_head.sort()
#uniq_head=uniq_head[0:100]
D1_binded_result=pd.DataFrame()

for head in uniq_head:
    D1_list = []
    D1_count_list = []
    D1_pos_list = []
    target_D1 = ty_df[ty_df.HEAD == head]

    this_D1_cand = list(target_D1.D1)

    this_D1_uniq = list(set(this_D1_cand))
    this_D1_uniq.sort()

    for D1 in this_D1_uniq:
        D1_df = target_D1[target_D1.D1 == D1]

        D1_list.append(D1)
        D1_count_list.append(this_D1_cand.count(D1))

        D1_df = D1_df.reset_index(drop=True)
        D1_pos_list.append(D1_df.iloc[0].D1_pos)
    D1_result=pd.DataFrame({"D1":this_D1_uniq,"Head":head, "D1_Count":D1_count_list, "D1_POS":D1_pos_list})
    D1_binded_result = D1_binded_result.append(D1_result,ignore_index=True)

D2_binded_result = pd.DataFrame()

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
    this_D2_uniq.sort()

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

        D2_result = pd.DataFrame({ "D2": D2_list, "D1": this_D1, "Head": this_head, "D2_Count": D2_count_list,"D1_POS": this_D1_POS, "D2_POS": D2_pos_list})

       D2_binded_result =D2_binded_result.append(D2_result, ignore_index=True)

D3_binded_result = pd.DataFrame()

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
    this_D3_uniq.sort()

    #Head, D1, D2가 고정된 상태에서 고유한 D3에 대한 정보를 저장하기 위한 리스트
    D3_list = []
    D3_count_list = []
    D3_pos_list = []
    for D3 in this_D3_uniq:
        #target_D3(Head, D1,D2가 고정된 것에서 D3를 갖는 column만 조회함
        D3_df=target_D3[target_D3.D3 == D3]
        D3_df = D3_df.reset_index(drop=True)
        D3_list.append(D3)
        D3_count_list.append(this_D3_list.count(D3))
        D3_pos_list.append(D3_df.iloc[0].D2_pos)

        D3_result = pd.DataFrame(
            {"D3": D3_list, "D2": this_D2, "D1": this_D1, "Head": this_head, "D3_Count": D3_count_list,
             "D3_POS": D3_pos_list, "D2_POS": this_D2_POS, "D1_POS": this_D1_POS})

    D3_binded_result =D3_binded_result.append(D3_result, ignore_index=True)

end = time.time()
print(end - start)

"""
word="WORD"
list1=[1,2,3,4]
pd.DataFrame({"Word":word,"LIST":list1})
"""

#time record: 1334.2329425811768

D3_binded_result.to_excel("190710_22분_NP_hierarchy.xlsx")