import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pulp import *


main_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_path)
df = pd.read_csv("material.csv",encoding="SHIFT-JIS")

viscosity = df["粘度"]
plt.hist(viscosity,color="blue",bins=20,rwidth=0.9)
# plt.show()

#モデル作製
prob = LpProblem(sense=LpMaximize)

material_list = df["原料ID"].tolist()
group_list = ["A","B","C","D","E"]

MG_list =[(m,g) for m in material_list for g in group_list]
x = LpVariable.dicts(name="x",indices=MG_list,cat="Binary")

#制約条件0.各原料は１つのグループのみに割り当てる
for m in material_list:
    prob += lpSum([x[m,g] for g in group_list]) == 1

#制約条件1.各グループの原料の数は20以上21以下
for g in group_list:
    prob += lpSum([x[m,g] for m in material_list]) >=20
    prob += lpSum([x[m,g] for m in material_list]) <=21


#制約条件2. 各グループの酸性、アルカリ性の原料は11以下とする。
acid_list = [row.原料ID for row in df.itertuples() if row.酸性flag==1]
alkaline_list = [row.原料ID for row in df.itertuples() if row.酸性flag==0]
for g in group_list:
    prob += lpSum([x[m,g] for m in acid_list]) <=11
    prob += lpSum([x[m,g] for m in alkaline_list]) <=11

#制約条件3. 各グループの平均粘度の差異を±10とする。
viscosity_dict = {row.原料ID:row.粘度 for row in df.itertuples()}
viscosity_mean = viscosity.mean()
tolerance = 10
for g in group_list:
    prob += lpSum([x[m,g]*viscosity_dict[m] for m in material_list]) >= (viscosity_mean-tolerance) * lpSum([x[m,g] for m in material_list])
    prob += lpSum([x[m,g]*viscosity_dict[m] for m in material_list]) <= (viscosity_mean+tolerance) * lpSum([x[m,g] for m in material_list])

# 制約条件4. 各グループに活性化特性を持つ原料を1以上とする
activate_list = [row.原料ID for row in df.itertuples() if row.活性化flag==1]
for g in group_list:
    prob += lpSum([x[m,g] for m in activate_list]) >= 1

# 制約条件5. 各グループに不活性化特性を持つ原料を1以下とする
unactivate_list = [row.原料ID for row in df.itertuples() if row.不活性化flag==1]
for g in group_list:
    prob += lpSum([x[m,g] for m in unactivate_list]) <= 1

status = prob.solve()
print(status)
print(LpStatus[status])

m_in_group = {}
for g in group_list:
    m_in_group[g] = [m for m in material_list if x[m,g].value()==1]

for group,materials in m_in_group.items():
    print("*"*15,"グループ",group,"*"*15)
    print("原料の数:",len(materials))
    print("原料ID:",materials)
    list = [df.iloc[material-1,2] for material in materials]
    print("平均粘度:",round(np.mean(list),1),f"({round(viscosity_mean,1)})")

