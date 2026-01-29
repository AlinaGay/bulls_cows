from operator import attrgetter
import random


N = 4

def generate_number():
    return random.randit(1000, 9999)


def add_to_context(
    attempt=1,
    guess_number=0,
    cows_number=0,
    bulls_number=0,
    guess_list=[]
):
    attempt_dict = {
        "Ход": {attempt},
        "Попытка": {guess_number},
        "Быки": {bulls_number},
        "Коровы": {cows_number}
    }
    return guess_list + attempt_dict


def analyze_bulls(secret_number, guess_number):
    bulls_dict = {
        i: x
        for i, (x, y) in (
            enumerate(zip(str(secret_number), str(guess_number))))
        if x == y}

    return len(bulls_dict)


def analyze_cows(secret_number, guess_number, bulls_number):
    cows_bulls_number = sum(
        1 for num in str(guess_number) if num in str(secret_number))

    return cows_bulls_number - bulls_number


def generate_guess(cows_number, bulls_number, guess_list):
    attempt = len(guess_list) + 1

