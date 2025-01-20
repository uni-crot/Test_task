# Test_task 
Здесь лежат скрипты для задания 3 про преобразование файла  

## Предобработка 
На вход подается файл FP_SNPs.txt, который имеет вид 
rs#	chromosome	GB37_position	GB38_position	allele1	allele2
2887286	1	1156131	1220751	C	T  

Из него надо получить файл FP_SNPs_10k_GB38_twoAllelsFormat.tsv с удаленными данными по X хромосоме и вида
#CHROM	POS	ID	allele1	allele2
chr1	1220751	rs2887286	C	T

Для этого используется скрипт на bash preprocess.sh, он лежит в репозитории с комментариями. 

