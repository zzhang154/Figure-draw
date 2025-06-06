# #!/bin/sh

read -p "请输入数据类型 (DCN 或 ISP): " data_type

if [ "$data_type" = "DCN" ]; then
    input_file1="extracted_tcpagg_dcn.txt"
    input_file2="extracted_cfnagg_dcn.txt"
    output_file="dcn_time_throughput.pdf"
elif [ "$data_type" = "ISP" ]; then
    input_file1="extracted_tcpagg_isp.txt"
    input_file2="extracted_cfnagg_isp.txt"
    output_file="isp_time_throughput.pdf"
else
    echo "无效的数据类型"
    exit 1
fi

gnuplot <<- EOF
    set datafile separator "\t"
    set bmargin at screen 0.2
    set lmargin at screen 0.18
    set rmargin at screen 0.95
    set style data linespoints
    set style fill solid 1.0 border -1
    set xtics nomirror
    set ytics nomirror
    set key above
    set key box width 0.5
    set key box font "Times_New_Roman, 16"
    set xlabel "Time(s)" font "Times_New_Roman, 24" offset 0, -0.5
    set ylabel "Throughput (Gbps)" font "Times_New_Roman, 24" offset -2.2, -1
    set xtics font "Times_New_Roman, 24"
    set ytics 1 font "Times_New_Roman, 24"
    set xrange [0:*]
    set yrange [6:10]
    set term pdfcairo
    set output "${output_file}"
    plot "${input_file1}" using (\$1/1000):(\$2/10) title "TCPAgg" with lines linetype 1 linecolor rgb "grey", \
         "${input_file2}" using (\$1/1000):(\$2/10) title "CFNAgg" with lines linetype 1 linecolor rgb "red"
EOF

echo "Plot generated: ${output_file}"