"""
1. Generate random num between 0 - 1 and 1 - 10
2. Use datetime lib together with the random number to generate a randon unique value
"""
from random import randint
import datetime 

num_a = randint(0, 1)
num_b = randint(1, 10)

dt = datetime.datetime.now()
dt  = str(num_b) + str(dt)
print(dt)