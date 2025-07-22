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
    num_random_digits = int(length) - len(prefix) - 1
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
    def test_valid_visa(self):
        for _ in range(10000):
            is_valid = random.choice([True, False])
            card = make_credit_card('4', 16, valid_check=is_valid)
            credit_card_validator(card)

    def test_valid_mastercard(self):
        for _ in range(10000):
            if random.random() < 0.5:
                prefix = str(random.randint(50, 56))
            else:
                prefix = str(random.randint(2220, 2721))
            is_valid = random.choice([True, False])
            card = make_credit_card(prefix, 16, valid_check=is_valid)
            credit_card_validator(card)

    def test_valid_amex(self):
        for _ in range(10000):
            prefix = random.choice(['34', '37'])
            is_valid = random.choice([True, False])
            card = make_credit_card(prefix, 15, valid_check=is_valid)
            credit_card_validator(card)

    def test_random_combos(self):
        base = ''.join(random.choices('0123456789', k=9))
        small_card = base + calculate_check_digit(base)
        credit_card_validator(small_card)

        base2 = ''.join(random.choices('0123456789', k=18))
        big_card = base2 + calculate_check_digit(base2)
        credit_card_validator(big_card)

        for _ in range(5000):
            length = random.randint(2, 20)
            base = ''.join(random.choices('0123456789', k=length - 1))
            luhn = calculate_check_digit(base)
            check = luhn if random.choice([True, False]) else random.choice(
                [d for d in '0123456789' if d != luhn]
            )
            credit_card_validator(base + check)


if __name__ == '__main__':
    unittest.main()
