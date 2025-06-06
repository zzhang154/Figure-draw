#!/usr/bin/env python3
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # 1. 询问用户选择数据类型（DCN 或 ISP）
    data_type = input("Enter data type (DCN or ISP): ").strip().upper()
    if data_type == "DCN":
        file_tcp   = "extracted_tcpagg_dcn.txt"
        file_cfn   = "extracted_cfnagg_dcn.txt"
        output_pdf = "dcn_time_throughput_python.pdf"
        y_label    = "Throughput (Gbps)"
        # DCN 的 throughput_raw 需要除以 10 得到 Gbps
        def convert_throughput(raw): return raw / 10.0
    elif data_type == "ISP":
        file_tcp   = "extracted_tcpagg_isp.txt"
        file_cfn   = "extracted_cfnagg_isp.txt"
        output_pdf = "isp_time_throughput_python.pdf"
        y_label    = "Throughput (Mbps)"
        # ISP 的 throughput_raw 直接就是 Mbps，无需除以 10
        def convert_throughput(raw): return raw
    else:
        print("Invalid data type, please enter DCN or ISP.")
        sys.exit(1)

    # 2. 检查文件是否存在
    for f in (file_tcp, file_cfn):
        if not os.path.exists(f):
            print(f"File not found: {f}")
            sys.exit(1)

    # 3. 用 whitespace 分隔来读取两列数据
    df_tcp = pd.read_csv(file_tcp, delim_whitespace=True, header=None,
                         names=["time_ms", "throughput_raw"])
    df_cfn = pd.read_csv(file_cfn, delim_whitespace=True, header=None,
                         names=["time_ms", "throughput_raw"])

    # 4. 转换到秒和正确的吞吐量单位
    df_tcp["time_s"]     = df_tcp["time_ms"] / 1000.0
    df_tcp["throughput"] = convert_throughput(df_tcp["throughput_raw"])

    df_cfn["time_s"]     = df_cfn["time_ms"] / 1000.0
    df_cfn["throughput"] = convert_throughput(df_cfn["throughput_raw"])

    # 5. 开始绘制
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"]   = 16

    fig, ax = plt.subplots(figsize=(9, 5))

    # 6. 绘制 RAIN 曲线（对应原 CFNAgg）：使用浅蓝色实线，粗线
    ax.plot(
        df_cfn["time_s"],
        df_cfn["throughput"],
        color="#0055cc",       # 浅蓝色
        linewidth=3.0,
        solid_capstyle="round",
        label="RAIN"
    )

    # 7. 绘制 TCP 曲线（对应原 TCPAgg）：使用橙红色短虚线 + 方块标记，粗线
    #    markevery 采样点减少，避免点过多
    mark_interval = max(len(df_tcp) // 50, 1)
    ax.plot(
        df_tcp["time_s"],
        df_tcp["throughput"],
        color="#ff7f0e",       # 经典橙色
        linewidth=3.0,
        linestyle=(0, (1, 1)), # 1 点实线 + 1 点空白 的短虚线
        marker="s",            # 方块标记
        markersize=6,
        markerfacecolor="#ff7f0e",
        markeredgecolor="#ff7f0e",
        markevery=mark_interval,
        label="TCP"
    )

    # 8. 设置网格（浅灰色虚线），并确保网格在曲线下方
    ax.grid(True, linestyle="--", linewidth=0.6, color="gray", alpha=0.7)
    ax.set_axisbelow(True)

    # 9. 设置坐标轴标签
    ax.set_xlabel("Time (s)", fontsize=34, labelpad=10)
    ax.set_ylabel(y_label, fontsize=30, labelpad=10)

    # 10. 设置刻度字体大小
    ax.tick_params(axis="x", labelsize=32)
    ax.tick_params(axis="y", labelsize=32)

    # 11. 对于 DCN，固定 Y 轴范围为 [6, 10]；ISP 则让 Matplotlib 自动选择
    if data_type == "DCN":
        ax.set_ylim(6, 10)

    # 12. 将图例放在图内部
    if data_type == "DCN":
        # 右上角，稍微下移
        ax.legend(
            loc="upper right",
            bbox_to_anchor=(0.98, 0.82),  # x=0.98, y=0.90
            frameon=True,
            edgecolor="black",
            fontsize=28
        )
    else:  # ISP
        # 右下角
        ax.legend(
            loc="lower right",
            bbox_to_anchor=(0.98, 0.02),  # x=0.98, y=0.02，可微调 y 做上下微移
            frameon=True,
            edgecolor="black",
            fontsize=28
        )

    # 13. 调整边距以防止标签或图例被截断
    plt.tight_layout()

    # 14. 保存为 PDF
    plt.savefig(output_pdf, dpi=300, format="pdf")
    print(f"Plot saved to {output_pdf}")

    plt.close(fig)

if __name__ == "__main__":
    main()
