#!/bin/bash
declare -a arr=("aws_frankfurt" "aws_nor_cal" "aws_ohio" "aws_oregon" "aws_sao_paulo" "aws_stockholm" "azure_brazil" "azure_france" "azure_japan_east" "azure_south_africa_north" "azure_us_east" "gcp_asia_east" "gcp_australia_southeast" "gcp_europe_north" "gcp_us_central" "gcp_us_south")
for i in "${arr[@]}"
do
echo "downloading $i"
hdfs dfs -get NMS_Experiments/16_hour_4_16_23/initial_outputs/"$i"_MappedOutput/part-r-00000 "$i"
done