# #!/bin/sh

read -p "请输入数据类型 (DCN 或 ISP): " data_type

input_file="${data_type}_iteration_throughput.csv"
output_file="${data_type}_iteration_throughput.pdf"

gnuplot <<- EOF
    set datafile separator ","
    # buttom 
    set bmargin at screen 0.2
    # left
    set lmargin at screen 0.18
    # right
    set rmargin at screen 0.95
    set style data linespoints
    set style fill solid 1.0 border -1  # 使用 solid 填充样式
    # set key out vert
    set xtics nomirror
    set ytics nomirror
    set key above
    set key box width 0.5
    set key box font "Times_New_Roman, 16"
    set xlabel "Completion Percentage(%)" font "Times_New_Roman, 24" offset 0, -0.5  # 添加百分比符号
    set ylabel "Throughput(KB)" font "Times_New_Roman, 24" offset -2.2, -1
    set xtics font "Times_New_Roman, 24"
    set ytics font "Times_New_Roman, 24"
    set xrange [0:100]  # 设置 x 轴范围为 0 到 100
    set xtics 0, 20, 100
    set yrange [0:*]  # 设置 y 轴范围为 0 到 1000
    # 获取数据文件的行数
    stats "iteration_runtime.csv" using 0 nooutput
    N = STATS_records    # 数据行数减去标题行


    # 绘制图表
    set term pdfcairo
    set output "${output_file}"
    # 绘制图表
    plot "${input_file}" using (\$0*100.0/N):(\$2/1000) title "TCP - qbic" with lines linetype 1 linecolor rgb "red", \
         "${input_file}" using (\$0*100.0/N):(\$3/1000) title "TCP - AIMD" with lines linetype 1 linecolor rgb "blue", \
         "${input_file}" using (\$0*100.0/N):(\$4/1000) title "ICN - AIMD" with lines linetype 1 linecolor rgb "green", \
         "${input_file}" using (\$0*100.0/N):(\$5/1000) title "CFNAgg - QS" with lines linetype 1 linecolor rgb "purple"
EOF

echo "Plot generated: ${output_file}"

