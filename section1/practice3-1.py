from pulp import *

prob = LpProblem("practice3",sense=LpMaximize)

#変数定義
x = LpVariable("x",lowBound=0)
y = LpVariable("y",lowBound=0)
z = LpVariable("z",lowBound=0)

# 目的関数
prob += 5*x + 3*y + 2*z

#制約条件
prob += 2*x + z <= 5
prob += x + 2*y <= 10
prob += y + z <= 8
prob += 2*z <= 12

status = prob.solve()

print(f"演算結果:{LpStatus[status]}")
print(f"Xの生産量{x.value()}")
print(f"Yの生産量{y.value()}")
print(f"Zの生産量{z.value()}")

print(f"利益{prob.objective.value()}")