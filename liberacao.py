import time

bloco = bytearray(10)

t6 = time.perf_counter_ns()
bloco.clear()
del bloco
t7 = time.perf_counter_ns()

tempo_ms = (t7 - t6) / 1000000

print("Tempo medido em ms:", tempo_ms)