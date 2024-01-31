import random

from locust import HttpUser, task, constant_pacing


class MyUser(HttpUser):
    wait_time = constant_pacing(1)
    host = 'https://somesite'

    @task
    def my_task(self):
        self.client.get("/")


# Генерируем случайное число пользователей
random_users = random.randint(10, 20)

# Указываем рампап
spawn_rate = 2

# Запускаем Locust с этим числом пользователей
if __name__ == "__main__":
    import os

    os.system(f"locust -f {__file__} --users {random_users} --spawn-rate {spawn_rate} --headless --run-time 1m")
