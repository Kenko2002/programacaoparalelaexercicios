from multiprocessing import Pool
import time

# Função de tarefa que será executada por cada subprocesso
def worker_function(task):
    """
    Função executada por cada subprocesso.

    Args:
        task: Tupla ou dados contendo informações sobre o intervalo ou parte da tarefa.

    Returns:
        O resultado do processamento da tarefa.
    """
    process_start_time = time.time()

    # Exemplo de processamento
    start, end, target = task
    for idx, num in enumerate(range(start, end), start=start):  
        if num == target:
            process_end_time = time.time()
            print(f"Tempo decorrido no processo: {process_end_time - process_start_time} segundos")
            return idx  # Resultado encontrado
    
    process_end_time = time.time()
    print(f"Tempo decorrido no processo: {process_end_time - process_start_time} segundos")
    return None  # Resultado não encontrado

def start_subprocesses(total_tasks, num_processes, task_generator, task_processor):
    """
    Inicializa e gerencia subprocessos para processar tarefas em paralelo.

    Args:
        total_tasks: Número total de tarefas a serem divididas entre os processos.
        num_processes: Número de processos paralelos a serem utilizados.
        task_generator: Função que cria uma lista de tarefas a partir dos dados de entrada.
        task_processor: Função executada por cada subprocesso.

    Returns:
        Resultados obtidos após o processamento das tarefas.
    """
    # Criar as tarefas (usando o gerador de tarefas fornecido)
    tasks = task_generator(total_tasks, num_processes)

    start_time = time.time()

    # Processar as tarefas em paralelo
    with Pool(processes=num_processes) as pool:
        results = pool.map(task_processor, tasks)

    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.4f} segundos")
    return results

def example_task_generator(total_numbers, num_processes):
    """
    Gera uma lista de tarefas com base nos dados de entrada.

    Args:
        total_numbers: O número total de elementos ou intervalos para processar.
        num_processes: Número de processos paralelos.

    Returns:
        Lista de tarefas a serem processadas pelos subprocessos.
    """
    chunk_size = total_numbers // num_processes
    target_number = total_numbers - 1  # Exemplo: Procurar o último número
    return [(i, min(i + chunk_size, total_numbers + 1), target_number) 
            for i in range(0, total_numbers, chunk_size)]

if __name__ == "__main__":
    # Configurações gerais
    TOTAL_NUMBERS = 50000000  # Número total de elementos
    NUM_PROCESSES = 4  # Número de processos paralelos

    # Inicializar subprocessos usando o template
    results = start_subprocesses(
        total_tasks=TOTAL_NUMBERS,
        num_processes=NUM_PROCESSES,
        task_generator=example_task_generator,
        task_processor=worker_function
    )

    # Verificar os resultados (exemplo para busca)
    found = next((res for res in results if res is not None), None)
    if found is not None:
        print(f"Número encontrado no índice {found}!")
    else:
        print("Número não encontrado.")
