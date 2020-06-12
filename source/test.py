from itertools import groupby

a = ['shot1_18','shot2_19','shot3_1','shot1_158','shot3_18','shot2_128','shot4_18','shot1_1899']
# a = ['geek_1', 'coder_2', 'geek_4', 'coder_3', 'pro_3']
a.sort()
a = [list(i) for j,i in groupby(a,lambda x: x.partition('_')[0])]
print(a)
