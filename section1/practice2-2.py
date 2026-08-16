from pulp import *

#モデル作製
prob = LpProblem("practice2",sense=LpMaximize)

#変数定義
x = LpVariable("x",lowBound=0)
y = LpVariable("y",lowBound=0)

#目的関数
prob += 100 * x + 150 * y #100x+150y=k

#制約条件
prob += x + 2 * y <= 6 #y=-1/2*x +3
prob += 2 * x + y <= 9 #y=-2x+9

#ソルバーの実行
status = prob.solve()
print(f"演算結果:{LpStatus[status]}")
print(f"x={x.value()}")
print(f"y={y.value()}")