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
    new_order = ["RAIN", "TCP", "RAIN-0.5", "TCP-0.5"]
    available_cols = [c for c in new_order if c in df.columns]
    df = df[available_cols]

    # 4) 准备画布 & Axes
    fig, ax = plt.subplots(figsize=(10, 6))
    n = len(df.index)
    bar_width = 0.18
    x = np.arange(n)

    # 5) 配置颜色与纹理
    colors = {
        "RAIN":    "#FF8080",  # 亮色调浅红
        "TCP":     "#444444",  # 深灰
        "RAIN-0.5":"#e5a370",  # 浅橙
        "TCP-0.5": "#888888"   # 较深灰
    }
    hatches = {
        "RAIN":     "//",     # RAIN 纹理
        "TCP":      "xxx",
        "RAIN-0.5": "\\\\\\\\",
        "TCP-0.5":  "---"
    }

    # 6) 画柱状
    for i, col in enumerate(available_cols):
        # label
        label_text = col

        if col.endswith("-0.5"):
            facecolor = 'none'
            edgecol   = colors[col]
        else:
            facecolor = colors[col]
            if col == "RAIN":
                edgecol = 'gray'  # RAIN 的纹理和轮廓都用灰色
            else:
                edgecol = 'black'

        ax.bar(
            x + i * bar_width,
            df[col],
            bar_width,
            label=label_text,
            color=facecolor,
            edgecolor=edgecol,
            hatch=hatches[col]
        )

    # 7) 强制 X 轴刻度对应索引值
    center_offset = (len(available_cols) - 1) * bar_width / 2
    ax.set_xticks(x + center_offset)
    ax.set_xticklabels(df.index.astype(int).tolist(), fontsize=22)

    # 8) 设置 X/Y 轴标题，并增大字体
    ax.set_xlabel("#producers", fontsize=38, labelpad=12)
    ax.set_ylabel("Total agg time (s)", fontsize=38, labelpad=12)

    # 9) 增大刻度数字字体
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=38)

    # 10) 打开网格，并将网格置于柱子下方
    ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    ax.set_axisbelow(True)

    # 11) 根据文件名是否包含 “DCN” 来动态指定图例的列数与字体大小
    if "DCN" in os.path.basename(csv_path):
        legend_ncol = 1
        legend_fontsize = 34
    else:
        legend_ncol = 2
        legend_fontsize = 25

    leg = ax.legend(
        loc='upper left',
        bbox_to_anchor=(-0.003, 1.02),
        ncol=legend_ncol,
        frameon=True,
        edgecolor='black',
        fontsize=legend_fontsize,
        labelspacing=0.2,
        columnspacing=0.5
    )
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_alpha(1)

    # 12) 收紧布局并保存为 PDF
    plt.tight_layout()
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_pdf = f"{base_name}.pdf"
    plt.savefig(output_pdf, dpi=300)
    print(f"已保存：{output_pdf}")

    plt.close(fig)
