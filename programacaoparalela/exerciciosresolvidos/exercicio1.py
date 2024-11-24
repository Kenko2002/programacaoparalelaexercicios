

'''
1) Dado uma lista de 50.000 numeros inteiros. Desenvolver um programa paralelo que localize um determinado número, com um speedup maior ou igual a 1,5
Retorno:
a posição onde o número foi encontrado, ou none se o número não estiver no vetor
'''
from multiprocessing import Pool
import time

# Função de busca
def find_number(task):
    process_start_time = time.time()
    
    start, end, target = task
    for idx, num in enumerate(range(start, end), start=start):  # Encontra o índice localizando a posição no intervalo
        if num == target:
            process_end_time = time.time()
            print(f"Tempo decorrido no processo: {process_end_time - process_start_time} segundos")
            return idx  # Retorna o índice onde o número foi encontrado
    process_end_time = time.time()
    print(f"Tempo decorrido no processo: {process_end_time - process_start_time} segundos")
    return None




if __name__ == "__main__":
    total_numbers = 50000000
    target_number = 49999999
    num_processes = 2  # Número de processos

    chunk_size = total_numbers // (num_processes)  

    # Criar as tarefas
    tasks = [(i, min(i + chunk_size, total_numbers + 1), target_number) 
             for i in range(0, total_numbers, chunk_size)]

    start_time = time.time()

    # Usar Pool para paralelizar a busca
    with Pool(processes=num_processes) as pool:
        results = pool.map(find_number, tasks)

    # Verificar o resultado
    found = next((res for res in results if res is not None), None)
    if found is not None:
        print(f"Número {target_number} encontrado no índice {found}!")
    else:
        print(f"Número {target_number} não encontrado.")

    end_time = time.time()
    print(f"Tempo decorrido: {end_time - start_time} segundos")
