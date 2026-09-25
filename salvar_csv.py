import time
import csv


bloco = bytearray(10)


# LEITURA 

t0 = time.perf_counter_ns()
soma = sum(bloco)
t1 = time.perf_counter_ns()

read_ms = (t1 - t0) / 1000000


# ESCRITA

padrao = b'teste ' * len(bloco)

t2 = time.perf_counter_ns()
bloco[:] = padrao
t3 = time.perf_counter_ns()

write_ms = (t3 - t2) / 1000000


# SALVAR CSV

arquivo_csv = f"resultados.csv" 

tamanhos_mb = list(range(100))
repeticoes = 10
cabecalho = ["tamanhos", "repetição", "read_ms", "write_ms"]

# Cada linha representa uma repetição para um determinado tamanho de bloco

with open(arquivo_csv, "w", encoding="utf-8", newline="") as arquivo:

    w = csv.writer(arquivo)
    w.writerow(cabecalho) 

    for mb in tamanhos_mb:

        for t in range(1, repeticoes + 1):

            w.writerow([
                mb,
                t,
                f"{read_ms:.6f}",
                f"{write_ms:.6f}",
            ])

