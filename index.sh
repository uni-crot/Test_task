#!/bin/bash

# Путь к файлу генома
GENOME_FILE="GRCh38.d1.vd1.fa"

# Индексация генома
samtools faidx "$GENOME_FILE"

# Разбиение генома на файлы для хромосом
for i in {1..22} X Y M
do
  samtools faidx "$GENOME_FILE" "chr$i" > "chr$i.fa"
done

# Индексация каждого файла
for i in {1..22} X Y M
do
  samtools faidx "chr$i.fa"
done

echo "Геном разделён и индексирован для хромосом."