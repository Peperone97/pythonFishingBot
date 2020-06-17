import  os
import signal
import time
from subprocess import Popen

def main():
    print("Start in 2 seconds")
    time.sleep(2)

    process = Popen(["python", "autoFishing.py"])

    input()

    os.kill(process.pid, signal.SIGTERM)

    print("End")

if __name__ == "__main__":
    main()