# Базовый образ
FROM ubuntu:22.04

# Установка зависимостей, очищение кеша apt и удаление временных файлов
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libncurses5-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    autoconf \
    automake \
    pkg-config \
    cmake \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Задача переменных окружения для директории с программами
ENV SOFT=/soft
WORKDIR $SOFT

# ===============================
# Установка samtools
# Версия: 1.21 (релиз от 2024-09-12)
# ===============================
RUN wget https://github.com/samtools/samtools/releases/download/1.21/samtools-1.21.tar.bz2 && \
    tar -jxf samtools-1.21.tar.bz2 && \
    rm samtools-1.21.tar.bz2 && \
    cd samtools-1.21 && \
    ./configure --prefix=$SOFT/samtools-1.21 && \
    make && make install && \
    cd / && rm -rf samtools-1.21

# ===============================
# Установка htslib
# Версия: 1.21 (релиз от 2024-09-12)
# ===============================
RUN wget https://github.com/samtools/htslib/releases/download/1.21/htslib-1.21.tar.bz2 && \
    tar -jxf htslib-1.21.tar.bz2 && \
    rm htslib-1.21.tar.bz2 && \
    cd htslib-1.21 && \
    ./configure --prefix=$SOFT/htslib-1.21 && \
    make && make install && \
    cd / && rm -rf htslib-1.21

# ===============================
# Установка libdeflate
# Версия: 1.23 (релиз от 2024-12-11)
# ===============================
RUN wget https://github.com/ebiggers/libdeflate/archive/refs/tags/v1.23.tar.gz && \
    tar -xvzf v1.23.tar.gz && \
    rm v1.23.tar.gz && \
    cd libdeflate-1.23 && \
    cmake -B build && \
    cmake --build build && \
    cmake --install build --prefix=/usr/local && \  
    cd / && rm -rf libdeflate-1.23

# ===============================
# Установка bcftools
# Версия: 1.21 (релиз от 2024-09-12)
# ===============================
RUN wget https://github.com/samtools/bcftools/releases/download/1.21/bcftools-1.21.tar.bz2 && \
    tar -jxf bcftools-1.21.tar.bz2 && \
    rm bcftools-1.21.tar.bz2 && \
    cd bcftools-1.21 && \
    ./configure --prefix=$SOFT/bcftools-1.21 && \
    make && make install && \
    cd / && rm -rf bcftools-1.21

# ===============================
# Установка vcftools
# Версия: 0.1.16 (релиз от 2018-08-02)
# ===============================
RUN wget https://github.com/vcftools/vcftools/releases/download/v0.1.16/vcftools-0.1.16.tar.gz && \
    tar -xvzf vcftools-0.1.16.tar.gz && \
    rm vcftools-0.1.16.tar.gz && \
    cd vcftools-0.1.16 && \
    ./configure --prefix=$SOFT/vcftools-0.1.16 && \
    make && make install && \
    cd / && rm -rf vcftools-0.1.16

# Добавление исполняемых файлов в PATH
ENV PATH=$SOFT/samtools-1.21/bin:$SOFT/htslib-1.21/bin:$SOFT/libdeflate-1.23/bin:$SOFT/bcftools-1.21/bin:$SOFT/vcftools-0.1.16/bin:$PATH

CMD ["bash"]
