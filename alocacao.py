import time

# bytearray() cria uma matriz de bytes que pode ser alterada após a criação.

# bytearray() cria um array sem nenhum byte
# bytearray(3) cria um array com 3 bytes zerados (b'\x00\x00\x00')
# bytearray([65, 66, 67]) cria um array com base em números (b'ABC')
# bytearray("olá", "utf-8") transforma um texto em uma sequência de bytes que você pode modificar.

tamanho = 1024

t0 = time.perf_counter_ns()
bloco = bytearray(tamanho)
t1 = time.perf_counter_ns()

alloc_ms = (t1 - t0) / 1000000
alloc_s = alloc_ms * 0.001

print("Quantidade de bytes: ", bloco)
print("Tempo de alocação em ms", alloc_ms)
print(list(bloco))