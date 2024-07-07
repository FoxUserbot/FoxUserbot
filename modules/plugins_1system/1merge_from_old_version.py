from pystyle import  Write, Colors
import random
import os

if os.path.isdir("plugins"):
    i = random.randint(10000, 99999)
    os.rename("plugins", f"modules_old_{i}")
    Write.Print(f"""[WARNING] Old incompatible modules (modules_old_{i}) detected!
[WARNING] Please rewrite them in a new format and upload them to the
[WARNING] ==> “.modules\plugins_2custom” directory.\n""", Colors.red_to_yellow, interval=0.0)