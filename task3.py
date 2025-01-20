import pysam
import os
import argparse
import time

def log_message(message):
    """
    Выводит сообщение с временной меткой.
    """
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}") # вывод в консоль

def find_ref_allele(chromosome, pos, fasta_dir):
    """
    Вспомогательная функция для получения референсного аллеля
    на заданной хромосоме и позиции, с использованием пути к FASTA-файлам.
    """
    fasta_path = os.path.join(fasta_dir, f"{chromosome}.fa")   # путь к fasta файлам
    # Проверка существования файла 
    if not os.path.exists(fasta_path):
        raise FileNotFoundError(f"Файл {fasta_path} не найден.")
    
    # Открытие файла с хромосомой chromosome
    fasta_file = pysam.Fastafile(fasta_path)

    # Извлечение референсного аллеля для хромосомы
    ref_allele = fasta_file.fetch(chromosome, pos - 1, pos)
    
    # Закрытие файла
    fasta_file.close()
    return ref_allele

def change_rewrite(input_tsv, output_tsv, fasta_dir):
    """
    Читает TSV файл, проверяет референсный аллель с помощью find_ref_allele
    и записывает новый файл в формате «#CHROM<TAB>POS<TAB>ID<TAB>REF<TAB>ALT».

    :param input_tsv: Путь к входному TSV файлу.
    :param output_tsv: Путь к выходному TSV файлу.
    :param fasta_dir: Путь к директории, содержащей файлы FASTA.
    """
    log_message(f"Начало обработки файла {input_tsv}")
    
    try:
        with open(input_tsv, 'r') as infile, open(output_tsv, 'w') as outfile:
            # Чтение заголовка входного файла, удаление символа переноса строки, разделение табуляцией
            header = infile.readline().strip().split("\t")
            
            # Проверка, что заголовок соответствует формату
            expected_header = ["#CHROM", "POS", "ID", "allele1", "allele2"]
            if header != expected_header:
                raise ValueError("Заголовок входного файла не соответствует формату.")

            # Запись нового заголовка в выходной файл
            outfile.write("#CHROM\tPOS\tID\tREF\tALT\n")
            
            # Обработка данных
            for line in infile:
                # Разделяем строку на колонки
                columns = line.strip().split("\t")
                chromosome = columns[0]  # #CHROM
                pos = int(columns[1])  # POS
                snp_id = columns[2]  # ID
                allele1 = columns[3]  # allele1
                allele2 = columns[4]  # allele2
                
                # Получение референсного аллеля
                ref_allele = find_ref_allele(chromosome, pos, fasta_dir)
                
                # Определение ALT 
                if ref_allele == allele1:
                    alt_allele = allele2
                elif ref_allele == allele2:
                    alt_allele = allele1
                else:
                    alt_allele = "."

                # Запись новой строки в выходной файл
                outfile.write(f"{chromosome}\t{pos}\t{snp_id}\t{ref_allele}\t{alt_allele}\n")
                
        log_message(f"Файл успешно обработан и сохранен в {output_tsv}")
    
    except FileNotFoundError as e:
        log_message(f"Ошибка: {e}")
    except Exception as e:
        log_message(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    # Создание парсера аргументов
    parser = argparse.ArgumentParser(
        description="Скрипт для перезаписи файла с восстановлением референсных аллелей"
    )
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Путь к входному TSV файлу."
    )
    parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Путь к выходному TSV файлу."
    )
    parser.add_argument(
        "-f", "--fasta_dir", 
        required=True, 
        help="Путь к директории, содержащей файлы FASTA."
    )

    # Разбор аргументов командной строки
    args = parser.parse_args()

    # Вызыв основной функции
    change_rewrite(args.input, args.output, args.fasta_dir)
