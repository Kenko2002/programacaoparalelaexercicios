'''
2) Dado um vetor de 50.000 inteiros. Desenvolver um programa paralelo que ordene esse vetor, com um speedup maior ou igual a 1,7
Retorno: vetor ordenado

'''


from multiprocessing import Pool, set_start_method
import time


def vetor_decrescente(tamanho):
    """Retorna um vetor decrescente de tamanho 'tamanho'."""
    if tamanho <= 0:
        raise ValueError("O tamanho do vetor deve ser maior que zero.")
    return list(range(tamanho - 1, -1, -1))

def merge(left, right):
    """Função para realizar a fusão (merge) de dois subvetores ordenados."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_helper(lista):
    """Função recursiva de Merge Sort para ser usada de forma sequencial."""
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2
    left = lista[:mid]
    right = lista[mid:]
    
    left_sorted = merge_sort_helper(left)
    right_sorted = merge_sort_helper(right)
    
    return merge(left_sorted, right_sorted)

def merge_sort_parallel(lista, num_processes):
    """Versão paralela do Merge Sort com controle explícito de processos."""
    # Usando o Pool para dividir o trabalho entre os processos
    chunk_size = len(lista) // num_processes
    chunks = [lista[i:i + chunk_size] for i in range(0, len(lista), chunk_size)]
    
    with Pool(num_processes) as pool:
        # Ordenar cada chunk em paralelo
        sorted_chunks = pool.map(merge_sort_helper, chunks)
    
    # Agora, fazer a fusão das partes ordenadas
    while len(sorted_chunks) > 1:
        sorted_chunks = [merge(sorted_chunks[i], sorted_chunks[i + 1]) 
                         for i in range(0, len(sorted_chunks), 2)]
    
    return sorted_chunks[0]

if __name__ == '__main__':
    # Isso é necessário para plataformas Windows, onde a inicialização 'spawn' é a única opção.
    set_start_method('spawn', force=True)  # Configura a inicialização do processo para 'spawn'
    
    lista = vetor_decrescente(1000000)  # Tamanho ajustado para 50.000 como no enunciado.
    
    start_time = time.time()
    
    # Definindo o número de processos como o número de núcleos disponíveis
    num_processes = 4
    
    lista_ordenada = merge_sort_parallel(lista, num_processes)
    
    end_time = time.time()
    
    print("Lista ordenada:", lista_ordenada)  # Exibindo apenas os primeiros 10 elementos para verificar
    print(f"Tempo da versão paralela com {num_processes} processos: {end_time - start_time} segundos")
