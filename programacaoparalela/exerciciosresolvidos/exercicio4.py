from multiprocessing import Pool
import numpy as np
import time


# Função para calcular a soma de prefixos de uma fatia do vetor
def compute_prefix_sum(task):
    start_idx, end_idx, array, offset = task
    partial_sum = np.cumsum(array[start_idx:end_idx])  # Soma cumulativa da fatia
    return partial_sum + offset  # Ajusta com o deslocamento acumulado


def start(num_processes,n):
    # Tamanho do vetor e número de processos

    # Gerar o vetor de entrada
    A = np.random.randint(1, 100, n)  # Vetor com valores aleatórios entre 1 e 100

    # Dividir o vetor em partes iguais para cada processo
    chunk_size = n // num_processes
    tasks = []
    offset = 0  # Acumular os offsets das somas anteriores

    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = n if i == num_processes - 1 else (i + 1) * chunk_size
        tasks.append((start_idx, end_idx, A, offset))
        offset += np.sum(A[start_idx:end_idx])  # Atualizar o offset

    start_time = time.time()

    # Processar as somas de prefixos em paralelo
    with Pool(processes=num_processes) as pool:
        partial_results = pool.map(compute_prefix_sum, tasks)

    # Combinar os resultados parciais
    B = np.concatenate(partial_results)

    end_time = time.time()

    # Validar os resultados
    expected_B = np.cumsum(A)  # Resultado esperado com soma cumulativa sequencial
    print(f"Resultados iguais: {np.array_equal(B, expected_B)}")

    # Exibir tempos e informações
    
    print("relatório de execução:")
    print(f"Num processos:{num_processes}")
    print(f"Tempo total: {end_time - start_time:.4f} segundos")
    print(f"Vetor de entrada (A): {A[:10]}...")  # Exibir apenas os primeiros 10 valores
    print(f"Vetor de soma de prefixos (B): {B[:10]}...")



if __name__ == '__main__':
    start(1,90000000) #1 processo vetor de 90 000 000
    start(2,90000000) #2 processo vetor de 90 000 000
