#!/usr/bin/env python3
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 全局 Matplotlib 配置
# -----------------------------
plt.rcParams['font.family'] = 'Times New Roman'

# -----------------------------
# 查找当前目录下所有 .csv 文件
# -----------------------------
csv_files = glob.glob("*.csv")
if not csv_files:
    print("当前目录中没有找到任何 CSV 文件。")
    exit(0)

# -----------------------------
# 对每个 CSV 文件执行绘图，并输出同名 PDF
# -----------------------------
for csv_path in csv_files:
    # 1) 读取 CSV，第一列作为索引
    df = pd.read_csv(csv_path, index_col=0)
    print(f"正在处理：{csv_path}，索引 = {df.index.tolist()}")

    # 2) 转数值并把毫秒 → 秒
    df = df.apply(lambda col: pd.to_numeric(col, errors='coerce'))
    df = df.dropna(axis=1, how='all')
    df = df / 1000.0

    # 3) 重排列顺序
    new_order = ["RAIN", "TCP", "RAIN-NS"]
    available_cols = [c for c in new_order if c in df.columns]
    df = df[available_cols]

    # 4) 准备画布 & Axes
    fig, ax = plt.subplots(figsize=(10, 6))
    n = len(df.index)
    bar_width = 0.20
    x = np.arange(n)

    # 5) 颜色与纹理（改为更亮的配色，纹理密度稍微加大）
    colors = {
        "RAIN":    "#FFC0C0",  # 更亮的浅粉红
        "TCP":     "#999999",  # 浅灰
        "RAIN-NS": "#D0E7F9",  # 更亮的浅蓝
    }
    hatches = {
        "RAIN":    "//",   # 双斜线，密度更大
        "TCP":     "\\\\", # 双反斜线，密度更大
        "RAIN-NS": "--",   # 双横线，密度更大
    }

    # 6) 画柱状
    for i, col in enumerate(available_cols):
        label_text = "RAIN-NS" if col == "RAIN-NS" else col
        ax.bar(
            x + i * bar_width,
            df[col],
            bar_width,
            label=label_text,
            color=colors[col],
            edgecolor='black',
            hatch=hatches[col]
        )

    # 7) X 轴刻度
    offset = (len(available_cols) - 1) * bar_width / 2
    ax.set_xticks(x + offset)
    ax.set_xticklabels(df.index.astype(int).tolist(), fontsize=20)

    # 8) 轴标签
    ax.set_xlabel("#stragglers(%)", fontsize=38, labelpad=12)
    ax.set_ylabel("Total agg time (s)", fontsize=36, labelpad=12)

    # 9) 刻度数字
    ax.tick_params(axis='x', labelsize=36)
    ax.tick_params(axis='y', labelsize=36)

    # 10) 网格 & 栅格置于柱子下方
    ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    ax.set_axisbelow(True)

    # 11) 先 tight_layout 收紧主图
    fig.tight_layout()
    fig.subplots_adjust(top=0.98)

    # 12) 用 ax.legend 把 legend 摆到 Axes 顶部外面
    num_items = len(available_cols)
    leg = ax.legend(
        loc='lower center',
        bbox_to_anchor=(0.5, 0.95),
        ncol=num_items,
        frameon=False,
        fontsize=32,
        labelspacing=0.2,
        columnspacing=0.8,
        handletextpad=0.2
    )

    # 13) 保存时加上 bbox_inches='tight'
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_pdf = f"{base_name}.pdf"
    fig.savefig(output_pdf, dpi=300, bbox_inches='tight')

    print(f"已保存：{output_pdf}")
    plt.close(fig)
