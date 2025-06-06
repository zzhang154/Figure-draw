#!/bin/sh

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
    set xlabel "Number" font "Times_New_Roman, 24" offset 0, -0.5
    set ylabel "Running Time(s)" font "Times_New_Roman, 24" offset -2.2, -1  # 修改单位为秒
    set xtics font "Times_New_Roman, 24"
    set xtics ("10" -0.1,"20" 0.9,"30" 1.9,"40" 2.9,"50" 3.9)  
    set ytics font "Times_New_Roman, 24"
    set yrange [0:*]  # 确保纵坐标从 0 开始
    # 这里一定要在{title_name}两端加上双引号，否则不会识别为字符串
    # set title "${title_name}" font "Times_New_Roman, 15"
    set key
    set term pdfcairo
    set output "pronumber_runtime.pdf"
    plot "pronumber_runtime.csv" every ::1::5 using (\$2/1000) title "TCP - qbic", \
         "pronumber_runtime.csv" every ::1::5 using (\$3/1000) title "TCP - AIMD", \
         "pronumber_runtime.csv" every ::1::5 using (\$4/1000) title "CFNAgg - AIMD", \
         "pronumber_runtime.csv" every ::1::5 using (\$5/1000) title "CFNAgg - QSF"
EOF

echo "Plot generated: pronumber_runtime.pdf"