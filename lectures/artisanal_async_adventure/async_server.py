import select
import socket
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from typing import *

def algorithm(n: int) -> int:
    return n + 42


Address = Tuple[str, int]
Task = TypeVar("Task")
TASKS: Deque[Task] = deque()
WAIT_READ: Dict[socket.socket, Task] = {}
WAIT_SEND: Dict[socket.socket, Task] = {}


async def handler(sock: socket.socket) -> None:
    while True:
        request: bytes = await async_recv(sock, 100)

        if not request.strip():
            sock.close()
            return
        number = int(request)
        result = algorithm(number)
        await async_send(sock, f"{result}\n".encode("ascii"))


async def server(address: Address) -> NoReturn:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = await async_accept(sock)
        print(f"connection from addr {addr}")
        add_task(handler(client))


class Can(Enum):
    read = auto()
    send = auto()


@dataclass
class Until:
    action: Can
    target: socket.socket

    def __await__(self):
        yield self.action, self.target


async def async_accept(sock: socket.socket) -> Tuple[socket.socket, Address]:
    await Until(Can.read, sock)
    return sock.accept()


async def async_recv(sock: socket.socket, num: int) -> bytes:
    await Until(Can.read, sock)
    return sock.recv(num)


async def async_send(sock: socket.socket, data: bytes) -> int:
    await Until(Can.send, sock)
    return sock.send(data)


def add_task(task: Task) -> None:
    TASKS.append(task)


def run() -> None:
    while any([TASKS, WAIT_READ, WAIT_SEND]):
        while not TASKS:
            can_read, can_send, _ = select.select(WAIT_READ, WAIT_SEND, [])
            for sock in can_read:
                add_task(WAIT_READ.pop(sock))
            for sock in can_send:
                add_task(WAIT_SEND.pop(sock))
        current_task = TASKS.popleft()
        try:
            action, target = current_task.send(None)
        except StopIteration:
            continue
        if action is Can.read:
            WAIT_READ[target] = current_task
        elif action is Can.send:
            WAIT_SEND[target] = current_task
        else:
            raise ValueError(f"Unexpected action {action!r}")


add_task(server(("localhost", 30303)))
run()
