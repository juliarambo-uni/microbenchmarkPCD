import time 

bloco_teste = bytearray(10)
padrao = b'teste ' * len(bloco_teste)

t2 = time.perf_counter_ns()
bloco_teste[:] = padrao
t3 = time.perf_counter_ns()

write_ms = (t3 - t2) / 1000000

print("Tempo de escrita: ", write_ms)
print("Tamanho após a escrita: ", len(bloco_teste))