import time


inicio = time.perf_counter_ns()

soma = sum(range(1000001))

fim = time.perf_counter_ns()

tempo_ns = fim - inicio
tempo_ms = tempo_ns / 1000000
tempo_s = tempo_ms * 0.001

print("Tempo em segundos:", tempo_s)


