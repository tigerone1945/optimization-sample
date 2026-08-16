from pulp import *

prob = LpProblem(sense=LpMinimize)

#変数定義
xa = LpVariable("xa",lowBound=0)
xb = LpVariable("xb",lowBound=0)
xc = LpVariable("xc",lowBound=0)
ya = LpVariable("ya",lowBound=0)
yb = LpVariable("yb",lowBound=0)
yc = LpVariable("yc",lowBound=0)


# 目的関数
prob += 5*xa + 6*xb +16*xc + 8*ya + 8*yb + 4*yc

#制約条件
prob += xa + xb + xc == 10
prob += ya + yb + yc == 20
prob += xa + ya == 14
prob += xb + yb == 10
prob += xc + yc == 6


status = prob.solve()

print(f"演算結果:{LpStatus[status]}")
print(f"工場X→支店A:{xa.value()}")
print(f"工場X→支店B:{xb.value()}")
print(f"工場X→支店C:{xc.value()}")
print(f"工場Y→支店A:{ya.value()}")
print(f"工場Y→支店B:{yb.value()}")
print(f"工場Y→支店C:{yc.value()}")

print(f"総輸送コスト:{prob.objective.value()}")