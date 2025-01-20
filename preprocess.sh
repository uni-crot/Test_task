#!/bin/bash

# Определение переменных для путей
INPUT_FILE="FP_SNPs.txt"
OUTPUT_FILE="FP_SNPs_10k_GB38_twoAllelsFormat.tsv"

# Операции с файлом
#сначала удаляются координаты по GRCh37, потом меняется порядок колонок в соотвествии с нужным (то что будет ID встает перед allele1), потом меняются названия колонок, добавляется префикс chr к значениям в #CHROM, префикс rs к третьей колонке - ID, после перезаписываются в новый файл первые 10000 строк (=удаляются строки по X хромосоме)
cut -f1,2,4- "$INPUT_FILE" | \
paste -d'\t' <(cut -f2,4 "$INPUT_FILE") \
             <(cut -f1 "$INPUT_FILE") \
             <(cut -f5- "$INPUT_FILE") | \
sed '1s/rs#/ID/; 1s/chromosome/#CHROM/; 1s/GB38_position/POS/' | \
sed '2,$s/^[0-9]/chr&/' | \
awk 'BEGIN {OFS="\t"} {if (NR == 1) print $0; else {$3="rs"$3; print}}' | \
head -n 10000 > "$OUTPUT_FILE"

echo "Результат сохранён в $OUTPUT_FILE"