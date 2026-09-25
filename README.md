# microbenchmarkPCD
Trabalho T2 da disciplina de Programação para Ciência de Dados: um microbenchmark que mede, em Python, quanto tempo o sistema operacional leva para alocar, escrever, ler e liberar blocos de memória, permitindo comparar os resultados entre Windows e Linux.

## O que é medido

O `benchmark.py` mede o tempo (com `time.perf_counter_ns`, em ms) de quatro operações de memória em Python:

| Operação | Código medido | Coluna no CSV |
|---|---|---|
| Alocação | `bloco = bytearray(bloco_bytes)` | `alloc_ms` |
| Escrita | `bloco[:] = padrao` | `write_ms` |
| Leitura | `sum(bloco)` | `read_ms` |
| Liberação | `bloco.clear()` e `del bloco` | `free_ms` |

Protocolo: blocos de 100, 200, ..., 1000 MB (10 tamanhos) × 100 repetições = 1.000 linhas por sistema.

## Como executar

O script usa apenas a biblioteca padrão do Python.

| Sistema | Comando | Saída |
|---|---|---|
| Windows | `python benchmark.py` | `resultados_windows.csv` e `ambiente_windows.json` |
| Linux | `python3 benchmark.py` | `resultados_linux.csv` e `ambiente_linux.json` |

O CSV tem as colunas `bloco_MB, teste, alloc_ms, write_ms, read_ms, free_ms`. O arquivo `ambiente_<sistema>.json` registra as condições do experimento (SO, CPU, versão do Python, início, fim e duração).

## Scripts de estudo

Arquivos usados para testar cada operação isoladamente, antes de montar o `benchmark.py`:

- `tempo.py` – uso básico do `time.perf_counter_ns`
- `alocacao.py`, `escrita.py`, `leitura.py`, `liberacao.py` – cada operação em um bloco pequeno
- `salvar_csv.py` – teste de gravação de resultados em CSV (gera `resultados.csv`)
