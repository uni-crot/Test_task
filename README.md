# Test_task 
Здесь лежат скрипты для задания 3 про преобразование файла  

## Предобработка 
На вход подается файл **FP_SNPs.txt**, который имеет вид  
rs#	chromosome	GB37_position	GB38_position	allele1	allele2  
2887286	1	1156131	1220751	C	T  

Из него надо получить файл **FP_SNPs_10k_GB38_twoAllelsFormat.tsv** с удаленными данными по X хромосоме и вида  
#CHROM	POS	ID	allele1	allele2  
chr1	1220751	rs2887286	C	T  

Для этого используется скрипт на bash **preprocess.sh**, он лежит в репозитории с комментариями. Скрипт нужен для удаления колонки GB37_position, перестановки колонки rs# перед allele1, переименовыванием chromosome в #CHROM, rs# в ID, GB38_position в POS, добавления префиксов chr к колонке #CHROM и rs к колонке ID, а также удаления строк по X хромосоме (удалили последние 1000 строк).  

Проверить количество записей по X хромосоме в разных файлах можно с помощью   
grep chr23 file_name | wc -l # сошлось, в исходном файле 1000, потом 0  
grep -c 'chr.*'  # сколько всего записей - 11000 в исзодном файле  


Референсный геном человека был скачан, разархивирован, разделен по хромосомам на отдельные файлы и проиндексирован. По итогу получились файлы типа chr[1-22,M,X,Y].fa[.fai]. Для этого использовался скрипт на bash **index.sh** (тоже в репозитории).  

## Преобразование файла к VCF-подобному формату  
Для этого используется скрипт **task3.py**. На вход подается 3 обязательных параметра: __input_tsv__ (файл, который надо преобразовать и распознать референсные аллели), __output_tsv__ (VCF-подобный выходной файл), __fasta_dir__ (путь к директории, где хранятся проиндексированные fasta файлы референсного генома).  

В рамках основного скрипта есть вспомогательная функция __find_ref_allele__(chromosome, pos, fasta_dir), которая на вход получает хромосому и позицию аллеля и находит в референсе значение для будущего REF. Реализована с использованием pysam.Fastafile.   

Функция __log_message__ нужна для создания временных меток работы программы и вывода информации в консоль. 

Функция __change_rewrite__ является основной. Из входного input_tsv файла берутся значения __chromosome__ и __pos__ для функции определения референсного аллеля __find_ref_allele__. В __output_tsv__ записывается уже преобразованный файл с заголовком #CHROM<TAB>POS<TAB>ID<TAB>REF<TAB>ALT, где в колонке REF стоит значение из __find_ref_allele__, а в ALT - второй аллель из входного файла.  

Скрипт можно запускать с консоли, требуется 3 обязательных аргумента командной строки:  -i INPUT -o OUTPUT -f FASTA_DIR. 

По результатам работы скрипта был получен файл **FP_SNPs_10k_GB38_RefAltformat.tsv**. Были обработаны все строки из входного **FP_SNPs_10k_GB38_twoAllelsFormat.tsv**. 
