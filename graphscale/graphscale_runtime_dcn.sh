#!/bin/sh

# ——————————————————————————————————————————————————————————
# 生成带图案的分组条形图 (Homa, Direct, ACP, Ours)
# 输入：CSV 文件，第一列是 Topology 名称，后面 4 列依次是 Homa/Direct/ACP/Ours 的 Cost
# 输出：一个 pdf（cairo）格式的直方图
# ——————————————————————————————————————————————————————————

read -p "请输入数据类型 (DCN 或 ISP): " data_type
input_file="${data_type}_graphscale_runtime.csv"
output_file="${data_type}_graphscale_runtime_bar.pdf"

gnuplot <<EOF
    ###############################
    # 1) 终端与输出
    ###############################
    set terminal pdfcairo enhanced font "Times-New-Roman,16" size 8in,5in
    set output "${output_file}"

    ###############################
    # 2) 数据 & 样式
    ###############################
    set datafile separator ","
    set style data histogram
    set style histogram clustered gap 1    # 分组
    set style fill pattern border         # 启用图案填充
    set boxwidth 0.8 relative             # 每组条宽度占 80%

    # 定义每条曲线的填充图案 (pattern 1–10)
    set style line 1 fillpattern 4 border -1   # Homa    (密集斜线)
    set style line 2 fillpattern 5 border -1   # Direct  (网格)
    set style line 3 fillpattern 2 border -1   # ACP     (水平条纹)
    set style line 4 fillpattern 3 border -1   # Ours    (垂直条纹)

    ###############################
    # 3) 坐标轴 & 网格 & 图例
    ###############################
    set xtics nomirror font "Times-New-Roman,14"
    set ytics nomirror font "Times-New-Roman,14"
    set grid ytics lt 0 lw 1 lc rgb "#DDDDDD"   # 背后灰色网格线

    set xlabel "Topology" font "Times-New-Roman,18" offset 0,-0.5
    set ylabel "Cost"     font "Times-New-Roman,18" offset -1.0,0

    set key above center horizontal box font "Times-New-Roman,14"

    ###############################
    # 4) 真正画图
    #    假设 CSV 格式：
    #      Topology, Homa, Direct, ACP, Ours
    #    如：
    #      nobel-germany,0.80,0.83,1.00,0.82
    #      germany50,     0.80,0.88,1.00,0.78
    #      brain,         1.00,1.01,1.00,0.99
    #
    ###############################
    plot \
      "${input_file}" using 2:xtic(1) title "Homa"   ls 1, \
      ""               using 3          title "Direct" ls 2, \
      ""               using 4          title "ACP"    ls 3, \
      ""               using 5          title "Ours"   ls 4
EOF

echo "Plot generated: ${output_file}"
