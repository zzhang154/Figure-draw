#!/bin/sh

# 获取用户输入
read -p "请输入数据类型 (DCN 或 ISP): " data_type

# 根据用户输入设置文件名
input_file="${data_type}_datascale_runtime.csv"
output_file="${data_type}_dataset_runtime.pdf"

gnuplot <<- EOF
    set datafile separator ","
    # bottom 
    set bmargin at screen 0.2
    # left
    set lmargin at screen 0.18
    # right
    set rmargin at screen 0.98
    set style data histogram
    set style fill solid 1.0 border -1  # 使用 solid 填充样式
    # set key out vert
    set xtics nomirror
    set ytics nomirror
    set key above
    set key box width 0.5
    set key box font "Times_New_Roman, 16"
    set xlabel "Datasets" font "Times_New_Roman, 24" offset 0, -0.5
    set ylabel "Total agg time(s)" font "Times_New_Roman, 24" offset -2.2, -1  # 修改单位为秒
    set xtics font "Times_New_Roman, 12"
    set xtics ("ResNet-18" 0,"ResNet-50" 1.0,"GPT-2" 2.0,"DeepSeek-R1 (1.5B)" 3.0)  
    set ytics 1,10,10000 font "Times_New_Roman, 20"  # 调整纵坐标轴刻度标签
    set yrange [0:*]  # 确保纵坐标从 0 开始
    set logscale y  # 将纵坐标轴设置为对数轴
    # 这里一定要在{title_name}两端加上双引号，否则不会识别为字符串
    # set title "${title_name}" font "Times_New_Roman, 15"
    set key
    set term pdfcairo
    set output "${output_file}"
    plot "${input_file}" every ::1::5 using 2 title "CFNAgg", \
         "${input_file}" every ::1::5 using 3 title "TCP", \
         "${input_file}" every ::1::5 using 4 title "TCP-NoAgg"
EOF

echo "Plot generated: ${output_file}"