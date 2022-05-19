import ctypes

player = ctypes.windll.kernel32
player.Beep(1000, 200)

import time

for i in range(8):
    time.sleep(1)
    player.Beep(1000, 200)