import pulp
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# モデル作成
# -----------------------------
prob = pulp.LpProblem("practice1", sense=pulp.LpMaximize)

# -----------------------------
# 変数
# -----------------------------
x = pulp.LpVariable("x", cat="Continuous")
y = pulp.LpVariable("y", cat="Continuous")

# -----------------------------
# 目的関数
# -----------------------------
prob += x + y # 目的関数 (例: x + y を最大化)
# -----------------------------
# 制約条件
# -----------------------------
prob += x - y + 1 == 0 # 
prob += 3 * x - y + 3 == 0 # y = 3 * x + 3

# -----------------------------
# 求解
# -----------------------------
status = prob.solve()

# -----------------------------
# 結果表示
# -----------------------------
print(f"演算結果: {pulp.LpStatus[status]}")
print(f"x = {pulp.value(x)}")
print(f"y = {pulp.value(y)}")

a = np.linspace(-5, 5, 20)
b1 = a + 1
b2 = 3 * a + 3
plt.plot(a, b1, label="x - y + 1 = 0")
plt.plot(a, b2, label="3 * x - y + 3 = 0")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.tight_layout()

output_path = Path(__file__).with_name("practice1_plot.png")
plt.savefig(output_path, dpi=150)
plt.show()