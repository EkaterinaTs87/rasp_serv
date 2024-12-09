import multiprocessing
import time
import random
import queue

class Task:
    def __init__(self, id, duration):
        self.id = id
        self.duration = duration  # Время выполнения задания

class Server:
    def __init__(self, id):
        self.id = id
        self.current_task = None
        self.remaining_time = 0

    def assign_task(self, task):
        self.current_task = task
        self.remaining_time = task.duration
        print(f"Задание с {task.duration} секундами выполнения направлено на Сервер {self.id}.")

    def tick(self):
        if self.current_task:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                print(f"Сервер {self.id} завершает выполнение задания {self.current_task.id}.")
                self.current_task = None

    def is_busy(self):
        return self.current_task is not None

    def status(self):
        if self.is_busy():
            return f"выполняет задание (осталось {self.remaining_time} сек.)"
        else:
            return "пусто"

def main():
    print("Добро пожаловать в симулятор распределенной системы.")
    num_servers = int(input("Введите количество серверов: "))
    servers = [Server(i + 1) for i in range(num_servers)]
    task_queue = multiprocessing.Queue()

    while True:
        print("\nСостояние серверов:")
        for server in servers:
            print(f"Сервер {server.id}: {server.status()}")

        print("Очередь заданий:", list(task_queue.queue) if not task_queue.empty() else "нет.")

        command = input("Команда (добавить <время> / выйти): ")
        if command.startswith("добавить"):
            _, duration = command.split()
            duration = int(duration)
            task = Task(len(task_queue.queue) + 1, duration)
            task_queue.put(task)
            assign_task_to_server(servers, task)

        elif command == "выйти":
            break

        # Обработка заданий
        for server in servers:
            if server.is_busy():
                server.tick()
            else:
                if not task_queue.empty():
                    next_task = task_queue.get()
                    assign_task_to_server(servers, next_task)

def assign_task_to_server(servers, task):
    available_servers = [server for server in servers if not server.is_busy()]
    if available_servers:
        chosen_server = random.choice(available_servers)
        chosen_server.assign_task(task)
    else:
        print(f"Задание {task.id} добавлено в очередь.")

if __name__ == "__main__":
    main()

