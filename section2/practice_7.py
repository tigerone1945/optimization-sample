from pulp import *
import pandas as pd
import os
main_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_path)
df = pd.read_csv("route_cost.csv",index_col=0)

prob = LpProblem(sense=LpMinimize)
N = len(df)

#変数定義
x = [[LpVariable(f"x({i},{j})",cat="Binary") for i in range(N)] for j in range(N)]
u = [LpVariable(f"u({i})",cat="Continuous",lowBound=1,upBound=N) for i in range(N)]

#目的関数
prob += lpSum(df.iloc[i,j] * x[i][j] for i in range(N) for j in range(N) if i!=j)

#制約条件
for i in range(N):
    prob += lpSum(x[i][j] for j in range(N) if i!=j) == 1

for j in range(N):
    prob += lpSum(x[i][j] for i in range(N) if i !=j ) == 1

for i in range(N):
    prob += x[i][i] == 0

BigM = 100

for i in range(N):
    for j in range(1,N):
        if i!=j:
            prob += u[i] + 1 -BigM *(1 - x[i][j]) <= u[j]

status = prob.solve()

print(f"演算結果:{LpStatus[status]}")
print(f"最小移動コスト:{prob.objective.value()}")

table = str.maketrans({
    "0":"A",
    "1":"B",
    "2":"C",
    "3":"D",
    "4":"E",
})

for i in range(N):
    for j in range(N):
        if i!=j:
            print(f"x[{i}][{j}]:".translate(table),f"{x[i][j].value()}")

for i in range(N):
    print(f"u[{i}]:".translate(table),f"{u[i].value()}")

#A→C→D→E→B