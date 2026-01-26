import random


N = 4

def generate_number():
    number = random.randit(1000, 9999)
    return number


def add_to_state(attempt, guess_list=[]):
    guess_list.append(attempt)
    return guess_list


def analyze_bulls(secret_number, attempt, bulls_dict={}):
    secret_number_list = list(secret_number)
    attempt_list = list(attempt)

    for i in range(len(secret_number_list)):
        if secret_number_list[i] == attempt_list[i]:
            bulls_dict[i] = secret_number_list[i]

    return bulls_dict


def analyze_cows(secret_number, attempt, cows_dict={}):
    secret_number_list = list(secret_number)
    attempt_list = list(attempt)

    for i in range(len(secret_number_list)):
        if (
            secret_number_list[i] != attempt_list[i]
            and attempt_list[i] in secret_number_list
        ):
            cows_dict[i] = secret_number_list[i]

    return cows_dict


def attempt(bulls_dict={}, cows_dict={}, guess_list=[]):
    attempt = []
    if guess_list != []:
        for i in range(N):
            if i in bulls_dict.keys():
                attempt.append(bulls_dict[i])



