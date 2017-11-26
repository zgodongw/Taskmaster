from subprocess import *
import time
import os, signal
from logging import Logger

prog = {}


def handlit(signal, frame):
    print("handling...")

def main():
    signal.signal(signal.SIGCHLD, handlit)
    Popen("ls")
    Popen("./filewriter")

if __name__ == '__main__':
    main()
    time.sleep(20)