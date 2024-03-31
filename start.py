from os import system
from time import sleep

while True:
    # system("clear && /home/stephen/skywatcher/.venv/bin/python -m src.main")
    system("/home/stephen/skywatcher/.venv/bin/python -m src.main")
    print("Restarting...")
    sleep(0.2)  # 200ms to CTR+C twice
