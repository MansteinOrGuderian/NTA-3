import numpy as np
import random
import math

def is_prime(current_number):
    if (current_number == 1 or current_number == 2):
        return False
    for divisor in range(2, int(math.sqrt(current_number)) + 1): #brutforce checking, if prime
        if (current_number % divisor == 0):
            return False
    return True



