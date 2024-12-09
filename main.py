import multiprocessing
import time
import random

# Класс для задания
class Task:
    def __init__(self, id, complexity):
        self.id = id
        self.complexity = complexity  # Время выполнения задания

    def execute(self):
        print(f"Task {self.id} started with complexity {self.complexity}")
        time.sleep(self.complexity)  # Симуляция выполнения задания
        print(f"Task {self.id} completed")

# Функция для работы процесса
def worker(task_queue, process_id):
    while True:
        task = task_queue.get()  # Извлечение задания из очереди
        if task is None:  # Условие завершения работы процесса
            print(f"Process {process_id} exiting")
            break
        task.execute()

# Функция для создания и распределения заданий
def main():
    num_processes = 4  # Количество процессов
    task_queue = multiprocessing.Queue()

    # Создание процессов
    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(task_queue, i))
        p.start()
        processes.append(p)

    # Генерация заданий
    num_tasks = 10
    for i in range(num_tasks):
        complexity = random.uniform(0.5, 2.0)  # Сложность задания (время выполнения)
        task = Task(i, complexity)
        task_queue.put(task)  # Добавление задания в очередь

    # Завершение процессов
    for _ in range(num_processes):
        task_queue.put(None)  # Отправка сигнала завершения для каждого процесса

    # Ожидание завершения всех процессов
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
