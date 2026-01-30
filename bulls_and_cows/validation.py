# bulls_and_cows/validation.py

def is_valid_number(value) -> bool:
    """
    Validate that input is a valid 4-digit number for Bulls and Cows game.

    Rules:
    - Must be exactly 4 digits
    - No repeating digits
    - No leading zero
    """
    if value is None:
        return False

    s = str(value)

    if len(s) != 4:
        return False

    if not s.isdigit():
        return False

    if s[0] == '0':
        return False

    if len(set(s)) != 4:
        return False

    return True
