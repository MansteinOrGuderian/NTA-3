import numpy as np
import random
import math
from datetime import datetime
from sympy import factorint, Matrix

def is_prime(current_number):
    if (current_number == 1 or current_number == 2):
        return False
    for divisor in range(2, int(math.sqrt(current_number)) + 1): # brutforce checking, if prime
        if (current_number % divisor == 0):
            return False
    return True

def generate_primes_up_to(upper_bound):
    primes = []
    for num in range(2, upper_bound):
        if is_prime(num):
            primes.append(num)
    return primes

def creating_factor_base(n):
    const = 3.38
    log_n = math.log(n)
    upper_bound = const * math.exp(0.5 * pow(log_n * math.log(log_n), 0.5)) # c * e^{(log(n) * log(log(n))) ^ 0.5 }
    return generate_primes_up_to(int(upper_bound))

def check_if_number_is_smoothness(value, factor_base):
    if value == 1:
        return False
    factors = factorint(value) #using inbuild function to factorize given number
    return all(factor in factor_base for factor in factors)




def main():
    alpha = int(input("Enter generator α: ")) # number to degree
    beta = int(input("Enter  β: ")) # number, that is in right side
    mod_number = int(input("Order of a group n: ")) # mod number

    factor_base = creating_factor_base(mod_number) # array of numbers
    print(factor_base)

if __name__ == "__main__":
    main()

