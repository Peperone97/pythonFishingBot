import sys
import time
import os
import signal
from subprocess import Popen

def main():

    print("Select the game (1/M/m Minecraft, 2/T/t Terraria):")
    game = input()

    print("Start in 2 seconds")
    time.sleep(2)

    print(sys.platform)

    if (game == "1" or game == "M" or game == "m" or game == "Minecraft"):
        process = Popen(["python", "autoFishing.py", "minecraft"])

    if (game == "2" or game == "T" or game == "t" or game == "Terraria"):
        if(sys.platform == "linux"):
            print("For now this function doesn't work on linux")
            exit(0)
        else:
            process = Popen(["python", "autoFishing.py", "terraria"])

    input()

    os.kill(process.pid, signal.SIGTERM)

if __name__ == "__main__":
    main()