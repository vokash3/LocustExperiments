import random
import time

import locust
from locust import User, task, constant_pacing, LoadTestShape, run_single_user, FastHttpUser
import locust_plugins
from locust_plugins.listeners import jmeter


@locust.events.init.add_listener
def on_locust_init(environment, **kwargs):
    jmeter.JmeterListener(env=environment, testplan="examplePlan")


class QALoadUser(FastHttpUser):
    fixed_count = random.randint(1, 5)
    wait_time = constant_pacing(30)
    host = 'https://somesite'

    @task
    def test_task(self):
        print(self.fixed_count)
        self.client.get("/")
        self.client.get("/music")
        self.client.get("/auto")
        self.client.get("/all")


class TestUser(User):
    # шаг нагрузки = 30 секунд
    # целевой RPS = 100
    # требуемое кол-во VU = 3000
    wait_time = constant_pacing(30)
    weight = 45

    @task
    def task(self):
        request_start_time = time.time()
        time.sleep(random.randint(1, 5))  # имитация времени ответа от 1 до 5 секунд
        processing_time = int((time.time() - request_start_time) * 1000)
        locust.events.request.fire(
            request_type="POST",
            name='TEST',
            response_time=processing_time,
            response_length=0,
            context=None,
            exception=None,
        )


class Test2User(User):
    # шаг нагрузки = 30 секунд
    # целевой RPS = 100
    # требуемое кол-во VU = 3000
    wait_time = constant_pacing(30)
    weight = 45

    @task
    def task(self):
        request_start_time = time.time()
        time.sleep(random.randint(1, 5))  # имитация времени ответа от 1 до 5 секунд
        processing_time = int((time.time() - request_start_time) * 1000)
        locust.events.request.fire(
            request_type="POST",
            name='TEST2',
            response_time=processing_time,
            response_length=0,
            context=None,
            exception=None,
        )


class Test3User(User):
    # шаг нагрузки = 30 секунд
    # целевой RPS = 100
    # требуемое кол-во VU = 3000
    wait_time = constant_pacing(30)
    weight = 10

    @task
    def task(self):
        request_start_time = time.time()
        time.sleep(random.randint(1, 5))  # имитация времени ответа от 1 до 5 секунд
        processing_time = int((time.time() - request_start_time) * 1000)
        locust.events.request.fire(
            request_type="POST",
            name='TEST3',
            response_time=processing_time,
            response_length=0,
            context=None,
            exception=None,
        )


class TestFastHttpUser(FastHttpUser):
    # шаг нагрузки = 30 секунд
    # целевой RPS = 20 или 1200 RPM
    # требуемое кол-во VU = 600
    host = "https://somesite"
    wait_time = constant_pacing(30)

    @task
    def get_main_page(self):
        self.client.get("/")


class LinearShape(LoadTestShape):
    stages = [
        {"duration": 30, "users": 3000, "spawn_rate": 100, "user_classes": [TestUser, Test2User]},
        {"duration": 60, "users": 3600, "spawn_rate": 20, "user_classes": [Test3User]},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None


class PacingTestShape(LoadTestShape):
    stages = \
        [
            {"duration": 600,
             "users": 3334,
             "spawn_rate": 111.111111,
             "user_classes": [TestUser, Test2User, Test3User]},
        ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None


if __name__ == "__main__":
    run_single_user(TestUser)
