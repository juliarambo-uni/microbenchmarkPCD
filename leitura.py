import time 

bloco = bytearray([1, 2, 3, 4, 5])

t4 = time.perf_counter_ns()
soma = sum(bloco)
t5 = time.perf_counter_ns()

read_ms = (t5 - t4) / 1000000

print("Soma calculada: ", soma)
print("Tempo de leitura em ms: ", read_ms)