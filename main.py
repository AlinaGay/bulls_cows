import random


def generate_number():
    number = 0
    while True:
        number = random.randit(1000, 9999)
        digits = str(number)

        if len(set(digits)) == 4:
            return number


def analyze(secret_number, attempt):
    guess_list = []
    guess_list.append(attempt)
    if attempt in guess_list:
        return "Please, try another number."
    if secret_number == attempt:
        return "Great! You have won!"

    guessed_number_dict = {}
    secret_number_list = list(secret_number)
    attempt_list = list(attempt)

    bulls, cows = 0, 0

    for i in range(len(secret_number_list)):
        if secret_number_list[i] == attempt_list[i]:
            bulls += 1
            guessed_number_dict[i] = secret_number_list[i]
        if ((attempt_list[i] in secret_number_list) and
           (secret_number_list[i] != attempt_list[i])):
            cows += 1

    return bulls, cows, guessed_number_dict


def attempt(bulls=None, cows=None, guessed_number_dict=None):
    attempt = 0
    if not bulls and cows and guessed_number_dict:
        attempt = generate_number()

