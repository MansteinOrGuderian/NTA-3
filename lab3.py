import numpy as np
import random
import math
from sympy import factorint, Matrix
import itertools
import time

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

def creating_factor_base(mod_number):
    const = 3.38
    log_n = math.log(mod_number)
    upper_bound = const * math.exp(0.5 * pow(log_n * math.log(log_n), 0.5)) # c * e^{(log(n) * log(log(n))) ^ 0.5 }
    return generate_primes_up_to(int(upper_bound))

def check_if_number_is_smoothness(value, factor_base):
    if value == 1:
        return False
    factors = factorint(value) #using inbuild function to factorize given number
    return all(factor in factor_base for factor in factors)

def find_smooth_linear_equation(generator_alpha, mod_number, factor_base):
    t = len(factor_base)
    while True:
        k = random.randint(0, mod_number - 1)
        alpha_k = pow(generator_alpha, k, mod_number)
        if check_if_number_is_smoothness(alpha_k, factor_base):
            factors = factorint(alpha_k)
            equation = [0] * (t + 1)
            equation[-1] = k
            for i, prime in enumerate(factor_base):
                if prime in factors:
                    equation[i] = factors[prime]
            return equation

def create_system_of_linear_equations(alpha, mod_number, factor_base):
    size_of_factor_base = len(factor_base)
    num_equations = size_of_factor_base + 10 # put in reserve a little bit more equation, to solve certainly 
    equations = []
    for _ in range(num_equations):
        equation = find_smooth_linear_equation(alpha, mod_number, factor_base)
        equations.append(equation)
    return equations

def find_invertible_square_submatrix(A): 
    A = np.array(A) # convert list to array
    size_of_factor_base = A.shape[1] - 1
    for indices in itertools.combinations(range(A.shape[0]), size_of_factor_base):
        submatrix = A[np.ix_(indices, range(size_of_factor_base))]
        if (np.linalg.matrix_rank(submatrix) == size_of_factor_base):
            return submatrix, A[np.array(indices), -1]
    raise TypeError("Not quadratic matrix with independend lines.")

def calculate_modular_inverse_matrix(A, mod_number): 
    A = Matrix(A.tolist())
    try:
        A_inv = A.inv_mod(mod_number - 1)
        return np.array(A_inv).astype(int)
    except:
        return None # matrix with 0

def solve_system_of_equations(equations, mod_number, alpha, factor_base):
    t = len(equations[0]) - 1
    while True:
        A = np.array([eq[:t] for eq in equations])
        b = np.array([eq[t] for eq in equations])
        M, b_vector = find_invertible_square_submatrix(np.column_stack((A, b)))
        M_inv = calculate_modular_inverse_matrix(M, mod_number)
        if M_inv is not None:
            x = np.dot(M_inv, b_vector) % (mod_number - 1)
            return [int(val) for val in x]
        else:
            equations = create_system_of_linear_equations(alpha, mod_number, factor_base)

def calculate_discrete_logarithm(alpha, beta, factor_base, logs, mod_number):
    t = len(factor_base)
    for l in range(mod_number):
        beta_alpha_l = (beta * pow(alpha, l, mod_number)) % mod_number
        if check_if_number_is_smoothness(beta_alpha_l, factor_base):
            factors = factorint(beta_alpha_l)
            d = [0] * t
            for i, prime in enumerate(factor_base):
                if prime in factors:
                    d[i] = factors[prime]
            log_beta = (sum(d[i] * logs[i] for i in range(t)) - l) % (mod_number - 1)
            return log_beta
    raise ValueError("No smooth number found. Increase amount of equations.")

def main():
    alpha = int(input("Enter generator α: ")) # number to degree
    beta = int(input("Enter β: ")) # number, that is in right side
    mod_number = int(input("Enter order of a group n: ")) # mod number

    factor_base = creating_factor_base(mod_number) # array of numbers
    #print(factor_base)
    equations = create_system_of_linear_equations(alpha, mod_number, factor_base)
    #print(equations)
    logs = solve_system_of_equations(equations, mod_number, alpha, factor_base)
    print("Logarithms, that used in factor base:")
    for prime, log in zip(factor_base, logs): # zip == creates tuple
        print(f"log_{alpha}({prime}) = {log}")

    start = time.perf_counter()
    log_beta = calculate_discrete_logarithm(alpha, beta, factor_base, logs, mod_number)
    stop = time.perf_counter()
    print(f"Total time: {stop - start} seconds")
    print(f"Result is: log_{alpha}({beta}) = {log_beta}")


if __name__ == "__main__":
    main()

