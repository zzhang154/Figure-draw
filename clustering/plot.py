
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
plt.rcParams['hatch.linewidth'] = 3.0  # 加粗条纹

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

    # 2) 将无法解析为数字的单元格 → NaN，再将原始值（毫秒）转换为秒
    df = df.apply(lambda col: pd.to_numeric(col, errors='coerce'))
    df = df.dropna(axis=1, how='all')
    df = df / 1000.0  # 毫秒 → 秒

    # 3) 重新排列列顺序：RAIN 在左，CLMAT 在右
    new_order = ["RAIN", "CLMAT"]
    available_cols = [c for c in new_order if c in df.columns]
    df = df[available_cols]

    # 4) 准备画布
    fig, ax = plt.subplots(figsize=(10, 6))
    n = len(df.index)
    bar_width = 0.30
    x = np.arange(n)

    # 5) 配置配色与纹理 - 空心柱状图风格
    #    - RAIN  使用暗一点的橘红色
    #    - CLMAT 使用灰蓝色
    colors = {
        "RAIN":  "#CC4125",  # 暗一点的橘红色
        "CLMAT": "#6495ED",  # 灰蓝色
    }
    hatches = {
        "RAIN":  "xxx",      # 交叉斜纹
        "CLMAT": "\\\\\\",   # 左斜纹
    }

    # 6) 绘制每个系列 - 空心柱状图
    for i, col in enumerate(available_cols):
        ax.bar(
            x + i * bar_width,
            df[col],
            bar_width,
            label=col,
            color='none',                           # 背景透明
            edgecolor=colors.get(col, "#777777"),   # 边框和纹理颜色
            hatch=hatches.get(col, ""),             # 纹理样式
            linewidth=2.0                           # 边框线宽
        )

    # 7) 强制 X 轴刻度对应索引值，并将其居中
    center_offset = (len(available_cols) - 1) * bar_width / 2
    ax.set_xticks(x + center_offset)
    ax.set_xticklabels(df.index.astype(int).tolist(), fontsize=24)  # 刻度数字设为 24 号

    # 8) 设置 X/Y 轴标题
    ax.set_xlabel("#producers", fontsize=36, labelpad=12)
    ax.set_ylabel("Total agg time (s)", fontsize=38, labelpad=12)

    # 9) 增大刻度数字字体
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=36)

    # 10) 打开网格，并将网格线放在柱子后方
    ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    ax.set_axisbelow(True)

    # 11) 图例放在图内部左上方，稍微往右移动一点
    leg = ax.legend(
        loc='upper left',
        bbox_to_anchor=(0.02, 0.98),
        ncol=1,
        frameon=True,
        edgecolor='black',
        fontsize=25,  # 图例文字仍为 20 号
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