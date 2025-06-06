#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遍历当前目录下所有 "*.csv" 文件，为每个文件绘制“Loss Rate (%) vs Runtime (s)”曲线，
并将图片保存为同名 PDF。曲线样式：
  - RAIN：绿色虚线 + 实心方块，图例文本放在前面
  - TCP ：橙色点划线 + 实心圆，图例文本放在后面
  - X 轴：Loss Rate (%) 分类刻度，等间隔
  - Y 轴：Runtime(ms) → s
"""

import glob
import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_one(csv_path):
    # 1. 读取 CSV
    df = pd.read_csv(csv_path, header=0)
    if df.shape[1] < 3:
        print(f"⚠️  {csv_path} 至少要有三列：Loss + RAIN_runtime + TCP_runtime，跳过该文件。")
        return

    # 2. X 轴：Loss Rate 分类刻度
    raw_loss = df.iloc[:, 0].astype(str).str.rstrip('%').tolist()  # e.g. ["0%", "0.01%", ...]
    x = list(range(len(raw_loss)))                  # [0,1,2,...] 等间隔

    # 3. Y 轴：把 RAIN(ms) 与 TCP(ms) 转成秒
    #    假设第二列是 RAIN，第三列是 TCP
    rain_s = df.iloc[:, 1].astype(float).values / 1000.0
    tcp_s  = df.iloc[:, 2].astype(float).values / 1000.0

    # 4. 配置全局字体
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"]   = 16

    fig, ax = plt.subplots(figsize=(8, 5))

    # 5. 绘制 RAIN（绿色虚线 + 实心方块）
    ax.plot(
        x, rain_s,
        color="#2ca02c",         # 绿色
        linestyle="--",          # 虚线
        marker="s",              # 方块
        markersize=8,
        markerfacecolor="#2ca02c",
        markeredgecolor="#2ca02c",
        linewidth=2.5,
        label="RAIN"
    )

    # 6. 绘制 TCP（橙色点划线 + 实心圆）
    ax.plot(
        x, tcp_s,
        color="#ff7f0e",         # 橙色
        linestyle="-.",          # 点划线
        marker="o",              # 圆圈
        markersize=8,
        markerfacecolor="#ff7f0e",
        markeredgecolor="#ff7f0e",
        linewidth=2.5,
        label="TCP"
    )

    # 7. 网格 & 轴标签
    ax.grid(True, linestyle="--", linewidth=0.6, color="gray", alpha=0.7)
    ax.set_axisbelow(True)

    ax.set_xlabel("Loss Rate (%)", fontsize=34, labelpad=6)
    ax.set_ylabel("Runtime (s)",     fontsize=36, labelpad=6)

    ax.set_xticks(x)
    ax.set_xticklabels(raw_loss, fontsize=30)
    ax.tick_params(axis="y", labelsize=30)

    # 8. 图例：左上角，白底半透明 + 灰色虚线边框，遵循“RAIN 先，TCP 后”
    leg = ax.legend(loc="upper left", fontsize=30, frameon=True)
    frame = leg.get_frame()
    frame.set_facecolor((1, 1, 1, 0.8))   # 白底80%不透明
    frame.set_edgecolor("gray")           # 边框灰色
    frame.set_linestyle("--")             # 虚线边框
    frame.set_linewidth(1.0)

    # 9. 保存为 PDF
    plt.tight_layout()
    base = os.path.splitext(os.path.basename(csv_path))[0]
    out_pdf = f"{base}.pdf"
    try:
        plt.savefig(out_pdf, dpi=300, format="pdf")
        print(f"✔ 已生成: {out_pdf}")
    except Exception as e:
        print(f"❌ 保存 PDF 失败: {out_pdf}，错误: {e}")

    plt.close(fig)


def main():
    # 遍历当前目录下所有 .csv
    for file in glob.glob("*.csv"):
        plot_one(file)


if __name__ == "__main__":
    main()
