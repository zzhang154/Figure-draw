#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter, FixedLocator, FixedFormatter

# -----------------------------
# 1. 读取 CSV
# -----------------------------
csv_name = "DCN_datascale_runtime.csv"
if not os.path.exists(csv_name):
    print(f"File not found: {csv_name}")
    exit(1)

df = pd.read_csv(csv_name, index_col=0)

# 去除列名/索引前后空格
df.columns = df.columns.str.strip()
df.index = df.index.astype(str).str.strip()

# 强制数值化并删除全 NaN 列
df = df.apply(lambda col: pd.to_numeric(col, errors='coerce'))
df = df.dropna(axis=1, how='all')

# -----------------------------
# 2. 使用全部4行（ResNet-18、ResNet-50、GPT-2、DeepSeek-R1 (1.5B)）
# -----------------------------
desired_order = ["RAIN", "TCP", "PS"]
available_cols = [c for c in desired_order if c in df.columns]
if not available_cols:
    print("Error: None of RAIN/TCP/PS found in columns!")
    exit(1)

df_plot = df[available_cols]

# -----------------------------
# 3. X 轴：4个位置
# -----------------------------
x = np.arange(len(df_plot.index))  # [0,1,2,3]
model_labels = [
    "ResNet\n-18",
    "ResNet\n-50",
    "GPT-2",
    "DeepSeek\n-R1(1.5B)"
]

# -----------------------------
# 4. 配色与纹理 - 空心柱状图，只显示纹理
# -----------------------------
colors = {
    "RAIN": "#CC4125",    # 稍微暗一点的橘红色
    "TCP":  "green",      # 绿色纹理
    "PS":   "#6495ED",    # 灰蓝色 (CornflowerBlue)
}
hatches = {
    "RAIN": "xxx",        # 交叉斜纹
    "TCP":  "///",        # 右斜纹
    "PS":   "\\\\\\",     # 左斜纹
}

# -----------------------------
# 5. 绘制柱状图
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.20

# 设置全局的hatch线宽
plt.rcParams['hatch.linewidth'] = 3.0  # 加粗条纹

for i, col in enumerate(available_cols):
    ax.bar(
        x + i * bar_width,
        df_plot[col].values,
        bar_width,
        label=col,
        color='none',                    # 背景透明
        edgecolor=colors[col],          # 边框和纹理颜色
        hatch=hatches[col],             # 纹理样式
        linewidth=2.0                   # 边框线宽
    )

# -----------------------------
# 6. 设置 X 轴刻度 & 标签
# -----------------------------
offset = (len(available_cols) - 1) * bar_width / 2.0
ax.set_xticks(x + offset)
ax.set_xticklabels(model_labels, fontsize=24)

# -----------------------------
# 7. 设置 X / Y 轴标题
# -----------------------------
ax.set_xlabel("Datasets", fontsize=38, labelpad=12)
ax.set_ylabel("Total agg time (s)", fontsize=36, labelpad=12)

# -----------------------------
# 8. 增大刻度字体
# -----------------------------
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=36)

# -----------------------------
# 9. 设置对数 Y 轴并自定义刻度显示 1, 10, 50, 100, 500, 1000, 2000
# -----------------------------
ax.set_yscale("log")

# 手动指定想要显示的刻度位置
custom_ticks = [1, 10, 100, 1000]
ax.set_yticks(custom_ticks)
ax.get_yaxis().set_major_formatter(FixedFormatter([str(t) for t in custom_ticks]))
ax.yaxis.grid(True, linestyle="--", linewidth=0.6, color="gray", alpha=0.7)
ax.set_axisbelow(True)

# -----------------------------
# 10. 图例
# -----------------------------
legend = ax.legend(
    loc="upper left",
    bbox_to_anchor=(0.02, 0.98),
    ncol=1,
    frameon=True,
    edgecolor="black",
    fontsize=22
)
legend.get_frame().set_facecolor("white")
legend.get_frame().set_alpha(1)

# -----------------------------
# 11. 保存为 PDF
# -----------------------------
plt.tight_layout()
out_pdf = "DCN_datascale_runtime.pdf"
plt.savefig(out_pdf, dpi=300)
print(f"Saved figure to: {out_pdf}")

plt.close(fig)