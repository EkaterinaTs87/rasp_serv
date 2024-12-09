import time
import random
from collections import deque

class Task:
    def __init__(self, id, duration):
        self.id = id
        self.duration = duration  # Время выполнения задания

class Server:
    def __init__(self, id):
        self.id = id
        self.current_task = None
        self.remaining_time = 0
        self.task_queue = deque()  # Очередь текущих заданий

    def assign_task(self, task):
        self.task_queue.append(task)
        if not self.current_task:  # Если сервер не занят, начинаем выполнение
            self.start_next_task()

    def start_next_task(self):
        if self.task_queue:
            self.current_task = self.task_queue.popleft()
            self.remaining_time = self.current_task.duration
            print(f"Задание с {self.current_task.duration} секундами выполнения направлено на Сервер {self.id}.")

    def tick(self):
        if self.current_task:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                print(f"Сервер {self.id} завершает выполнение задания {self.current_task.id}.")
                self.current_task = None
                self.start_next_task()  # Начинаем следующее задание

    def is_busy(self):
        return self.current_task is not None

    def total_remaining_time(self):
        return sum(task.duration for task in self.task_queue) + (self.remaining_time if self.current_task else 0)

    def status(self):
        if self.is_busy():
            return f"выполняет задание (осталось {self.remaining_time} сек.)"
        else:
            return "пусто"

def main():
    print("Добро пожаловать в симулятор распределенной системы.")
    num_servers = int(input("Введите количество серверов: "))
    servers = [Server(i + 1) for i in range(num_servers)]

    while True:
        print("\nСостояние серверов:")
        for server in servers:
            print(f"Сервер {server.id}: {server.status()}")

        print("Очереди заданий:")
        for server in servers:
            print(f"Сервер {server.id} очередь: {[task.id for task in server.task_queue]}")

        command = input("Команда (добавить <время> / выйти): ")
        if command.startswith("добавить"):
            _, duration = command.split()
            duration = int(duration)
            task = Task(len([t for s in servers for t in s.task_queue]) + 1, duration)
            assign_task_to_server(servers, task)

        elif command == "выйти":
            break

        # Обработка заданий
        for server in servers:
            server.tick()

def assign_task_to_server(servers, task):
    # Находим сервер с минимальным суммарным временем выполнения
    chosen_server = min(servers, key=lambda server: server.total_remaining_time())
    chosen_server.assign_task(task)

if __name__ == "__main__":
    main()

