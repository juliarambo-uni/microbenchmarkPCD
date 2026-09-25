"""
ETAPA 1 - EXECUTAR E COLETAR
=============================

OBJETIVO DESTE ARQUIVO
----------------------
Medir quanto tempo o sistema operacional (Windows ou Linux) leva para executar
quatro operações de memória em Python:

    1. ALOCAÇÃO  -> bloco = bytearray(bloco_bytes)   (reservar o espaço)
    2. ESCRITA   -> bloco[:] = padrao                (gravar bytes no espaço)
    3. LEITURA   -> sum(bloco)                       (percorrer e ler os bytes)
    4. LIBERAÇÃO -> bloco.clear() e del bloco         (devolver o espaço)

Isso é um "microbenchmark": um experimento pequeno e controlado que mede uma
única coisa de cada vez, sempre do mesmo jeito, para que os resultados de
Windows e Linux possam ser comparados de forma justa.

PROTOCOLO 
------------------------------
    - Tamanhos de bloco: 100, 200, ..., 1000 MB  (10 tamanhos)
    - Repetições: 100 para cada tamanho
    - Total: 10 x 100 = 1.000 linhas no CSV de cada sistema
    - Cada linha do CSV = UMA repetição de UM tamanho
    - Arquivos com nomes diferentes para Windows e Linux

O QUE ESTE SCRIPT GERA
----------------------
    resultados_windows.csv   (se rodar no Windows)  ou
    resultados_linux.csv     (se rodar no Linux)

COMO EXECUTAR
-------------
    Windows:  python benchmark.py
    Linux:    python3 benchmark.py

    
"""

import sys
import platform
from datetime import datetime
import csv
import gc
import time
import os
import json


TAMANHOS_MB = list(range(100, 1001, 100))
REPETICOES = 100
CABECALHO = ["bloco_MB", "teste", "alloc_ms", "write_ms", "read_ms", "free_ms"]


def nome_do_sistema():
    return platform.system().lower()


def medir_uma_repeticao(mb, padrao):
    
    bloco_bytes = mb * 1024 * 1024

    # ALOCAÇÃO 
    t0 = time.perf_counter_ns()
    bloco = bytearray(bloco_bytes)
    t1 = time.perf_counter_ns()

    alloc_ms = (t1 - t0) / 1_000_000


    # ESCRITA 
    t2 = time.perf_counter_ns()
    bloco[:] = padrao
    t3 = time.perf_counter_ns()

    write_ms = (t3 - t2) / 1_000_000


    # LEITURA 
    t4 = time.perf_counter_ns()
    soma = sum(bloco)
    t5 = time.perf_counter_ns()

    read_ms = (t5 - t4) / 1_000_000


    # LIBERAÇÃO
    t6 = time.perf_counter_ns()
    bloco.clear()
    del bloco
    t7 = time.perf_counter_ns()
    
    free_ms = (t7 - t6) / 1_000_000
    

    return alloc_ms, write_ms, read_ms, free_ms


def registrar_ambiente(caminho, inicio, fim):

    ambiente = {
        "sistema": platform.system(),          
        "versao_sistema": platform.release(),    
        "detalhe_sistema": platform.version(),   
        "maquina": platform.machine(),           
        "processador": platform.processor(),   
        "cpus_logicas": os.cpu_count(),          
        "python": platform.python_version(),   
        "implementacao_python": platform.python_implementation(),  
        "tamanhos_MB": TAMANHOS_MB,
        "repeticoes": REPETICOES,
        "relogio": "time.perf_counter_ns",
        "unidade_tempo": "ms",
        "inicio": inicio.isoformat(timespec="seconds"),
        "fim": fim.isoformat(timespec="seconds"),
        "duracao_min": round((fim - inicio).total_seconds() / 60, 2),
    }
    
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(ambiente, arquivo, ensure_ascii=False, indent=2)


# Função principal

def main():

    so = nome_do_sistema()
    arquivo_csv = f"resultados_{so}.csv"     
    arquivo_json = f"ambiente_{so}.json"     

    total = len(TAMANHOS_MB) * REPETICOES
    print(f"Sistema detectado: {platform.system()}")
    print(f"Gravando em: {arquivo_csv}  ({total} medições previstas)")

    inicio = datetime.now()
    contador = 0

    with open(arquivo_csv, "w", encoding="utf-8", newline="") as arquivo:
        w = csv.writer(arquivo)     
        w.writerow(CABECALHO)       

        for mb in TAMANHOS_MB:
           
            padrao = b"\xAA" * (mb * 1024 * 1024)

           
            for t in range(1, REPETICOES + 1):
              
                gc.collect()

                alloc, write, read, free = medir_uma_repeticao(mb, padrao)

                w.writerow([
                    mb,
                    t,
                    f"{alloc:.6f}",
                    f"{write:.6f}",
                    f"{read:.6f}",
                    f"{free:.6f}",
                ])

                contador += 1

            arquivo.flush()
            del padrao

            decorrido = (datetime.now() - inicio).total_seconds() / 60
            print(f"  {mb:>4} MB concluído | {contador}/{total} medições | "
                  f"{decorrido:.1f} min decorridos")

    fim = datetime.now()
    registrar_ambiente(arquivo_json, inicio, fim)

    print(f"\nColeta finalizada em {(fim - inicio).total_seconds() / 60:.1f} min.")
    print(f"CSV:      {arquivo_csv}")
    print(f"Ambiente: {arquivo_json}")


if __name__ == "__main__":
    main()
