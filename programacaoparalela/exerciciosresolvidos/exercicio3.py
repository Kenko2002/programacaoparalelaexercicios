import numpy as np
from multiprocessing import Process, Array
import time


def matrix_multiply_shared(chunk_index, rows_start, rows_end, shared_a, shared_b, shared_result, shape_a, shape_b):
    """
    Multiplica uma fatia da matriz A por B usando memória compartilhada.
    """
    rows_a, cols_a = shape_a
    cols_b = shape_b[1]
    
    # Reconstruir as matrizes a partir dos buffers compartilhados
    A = np.frombuffer(shared_a).reshape((rows_a, cols_a))
    B = np.frombuffer(shared_b).reshape((cols_a, cols_b))
    result = np.frombuffer(shared_result).reshape((rows_a, cols_b))
    
    # Calcular o chunk
    result[rows_start:rows_end] = np.dot(A[rows_start:rows_end], B)


def parallel_matrix_multiplication_shared(A, B, num_processes=None):
    """
    Multiplica matrizes A e B paralelamente usando memória compartilhada.
    """
    assert A.shape[1] == B.shape[0], "Número de colunas de A deve ser igual ao número de linhas de B"
    
    rows_a, cols_a = A.shape
    cols_b = B.shape[1]
    
    # Determinar o número de processos
    if num_processes is None:
        num_processes = 1  # Número padrão de processos
    
    # Criar memória compartilhada para as matrizes
    shared_a = Array('d', A.ravel(), lock=False)
    shared_b = Array('d', B.ravel(), lock=False)
    shared_result = Array('d', rows_a * cols_b, lock=False)
    
    # Dividindo as linhas de A para processamento em chunks
    chunk_size = rows_a // num_processes
    processes = []
    
    for i in range(num_processes):
        rows_start = i * chunk_size
        rows_end = (i + 1) * chunk_size if i != num_processes - 1 else rows_a
        
        process = Process(
            target=matrix_multiply_shared,
            args=(i, rows_start, rows_end, shared_a, shared_b, shared_result, A.shape, B.shape)
        )
        processes.append(process)
        process.start()
    
    # Aguardar todos os processos concluírem
    for process in processes:
        process.join()
    
    # Reconstituir a matriz resultante
    result_matrix = np.frombuffer(shared_result).reshape((rows_a, cols_b))
    return result_matrix


if __name__ == "__main__":
    # Matrizes de entrada
    rows_a, cols_b = 20000, 10000
    common_dim = 400
    num_processes= 4   #define o numero de processos
    
    # Inicializar matrizes com valores aleatórios
    np.random.seed(42)  # Para reprodutibilidade
    A = np.random.rand(rows_a, common_dim)
    B = np.random.rand(common_dim, cols_b)

    # Multiplicação paralela
    start_time = time.time()
    result = parallel_matrix_multiplication_shared(A, B, num_processes)
    end_time = time.time()

    # Exibir resultados
    print(f"Matriz resultante: {result.shape}")
    print(result)
    print(f"Tempo total: {end_time - start_time:.2f} segundos")
