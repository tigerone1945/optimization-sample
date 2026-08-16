#重量制限1200　として価値を最大化するようにitemを選びたい
from pulp import *
import pandas as pd
import os

main_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_path)
df = pd.read_csv("item_list.csv")

dict_weight = df.set_index("Name")["Weight"].to_dict()
dict_value = df.set_index("Name")["Value"].to_dict()

#モデル作製
prob = LpProblem(sense=LpMaximize)
#変数定義
dict_x = LpVariable.dicts(name="x",indices=df["Name"],cat="Binary")
print(dict_x)
# {'A': x_A, 'B': x_B, 'C': x_C, 'D': x_D, 'E': x_E, 'F': x_F, 'G': x_G, 'H': x_H, 'I': x_I, 'J': x_J, 'K': x_K, 'L': x_L, 'M': x_M, 'N': x_N, 'O': x_O}
#目的関数
prob += lpSum([dict_x[i]*dict_value[i] for i in dict_x.keys()])
#制約条件
prob += lpSum([dict_x[i]*dict_weight[i] for i in dict_x.keys()]) <= 1200

status = prob.solve()

print(LpStatus[status])
print([(key,value.value()) for key,value in dict_x.items()])
print(prob.objective.value())