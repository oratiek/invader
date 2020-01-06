import pygame
import time
from time import sleep
import numpy as np

def main():
    running = True
    counter = 0
    while running:
        counter += 1
        sleep(1)
        print("Counter : ",counter)
        if counter == 3:
            running = False
    if np.random.randint(2) == 0:
        print("Clear")
        return True
    else:
        print("Game over")
        return False


main_stream = True
level = 1
while main_stream:
    print("Level : ",level)
    clear = main()
    if clear == False:
        break
    level += 1

    
