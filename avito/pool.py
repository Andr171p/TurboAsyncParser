import threading

from typing import List


def create_task(data: list, thread_size: int) -> List[list]:
    tasks = [
        data[i:i+thread_size] for i in range(0, len(data), thread_size)
    ]
    return tasks



