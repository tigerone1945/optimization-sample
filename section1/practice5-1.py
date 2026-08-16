from pulp import *

prob = LpProblem(sense=LpMaximize)

list_item = ["A","B","C","D"]
list_weight = [3,6,5,7]
list_value = [4,7,6,8]

capacity = 15

#変数定義
list_x = [LpVariable(f"{item}",cat="Binary") for item in list_item]
#[A,B,C,D] =[1,0,1,0]

#目的関数
prob += lpSum([list_x[i]*list_value[i] for i in range(len(list_x))])

#制約条件
total_weight = lpSum([list_weight[i]*list_x[i] for i in range(len(list_x))])
prob += total_weight <=capacity

status = prob.solve()
print("演算結果:",LpStatus[status])
print([x.value() for x in list_x])
print(prob.objective.value())