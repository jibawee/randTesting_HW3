import unittest
import random
from credit_card_validator import credit_card_validator


def calculate_check_digit(number_without_check):
    total = 0
    reverse_digits = list(map(int, number_without_check[::-1]))
    for index, digit in enumerate(reverse_digits):
        if index % 2 == 0:
            total += digit
        else:
            doubled = digit * 2
            total += doubled if doubled < 10 else doubled - 9
    return str((10 - (total % 10)) % 10)


def make_credit_card(prefix, length, valid_check=True):
    num_random_digits = length - len(prefix) - 1
    middle = ''.join(random.choice('0123456789') for _ in range(num_random_digits))
    partial = prefix + middle
    correct_digit = calculate_check_digit(partial)

    if valid_check:
        check_digit = correct_digit
    else:
        invalid_choices = [d for d in '0123456789' if d != correct_digit]
        check_digit = random.choice(invalid_choices)

    return partial + check_digit


class TestCreditCardValidator(unittest.TestCase):

    def test_visa(self):
        for _ in range(1500):
            is_valid = random.choice([True, False])
            length = random.randint(13, 19)
            card = make_credit_card('4', length, valid_check=is_valid)
            credit_card_validator(card)

    def test_mastercard(self):
        for _ in range(1500):
            if random.random() < 0.5:
                prefix = str(random.randint(51, 55))
            else:
                prefix = str(random.randint(2221, 2720))
            is_valid = random.choice([True, False])
            length = random.randint(13, 19)
            card = make_credit_card(prefix, length, valid_check=is_valid)
            credit_card_validator(card)

    def test_amex(self):
        for _ in range(1500):
            prefix = random.choice(['34', '37'])
            is_valid = random.choice([True, False])
            length = random.randint(13, 19)
            card = make_credit_card(prefix, length, valid_check=is_valid)
            credit_card_validator(card)


if __name__ == '__main__':
    unittest.main()
