from operator import attrgetter
import random


N = 4

def generate_number():
    return random.randit(1000, 9999)


def add_to_state(attempt=1, guess_number=0, cows_number=0, bulls_number=0, guess_list=[]):
    return guess_list + [attempt]


def analyze_bulls(secret_number, guess_number):
    # secret_number_list = list(secret_number)
    # attempt_list = list(attempt)
    bulls_dict = {i: x for i, (x, y) in enumerate(zip(str(secret_number), str(guess_number))) if x == y}
    # for i in range(len(secret_number_list)):
    #     if secret_number_list[i] == attempt_list[i]:
    #         bulls_dict[i] = secret_number_list[i]

    return len(bulls_dict)


def analyze_cows(secret_number, guess_number, bulls_number):
    # secret_number_list = list(secret_number)
    # attempt_list = list(attempt)

    # for i in range(len(secret_number_list)):
    #     if (
    #         secret_number_list[i] != attempt_list[i]
    #         and attempt_list[i] in secret_number_list
    #     ):
    #         cows_dict[i] = secret_number_list[i]
    cows_bulls_number = sum(
        1 for num in str(guess_number) if num in str(secret_number))

    return cows_bulls_number - bulls_number


def generate_guess(cows_number, bulls_number, guess_list):
    attempt = len(guess_list) + 1
    
    



