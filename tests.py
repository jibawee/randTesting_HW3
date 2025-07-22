import unittest
import random
from credit_card_validator import credit_card_validator


def checkdigit(nocheck):
    total = 0
    reverse_digits = list(map(int, nocheck[::-1]))
    for index, digit in enumerate(reverse_digits):
        if index % 2 == 0:
            total += digit
        else:
            doubled = digit * 2
            total += doubled if doubled < 10 else doubled - 9
    return str((10 - (total % 10)) % 10)


def make_credit_card(prefix, length, valid_check=True):
    num_random_digits = int(length) - len(prefix) - 1
    base = ''.join(random.choice('0123456789') for _ in range(num_random_digits))
    partial = prefix + base
    correct_digit = checkdigit(partial)

    if valid_check:
        check_digit = correct_digit
    else:
        invalid_choices = [d for d in '0123456789' if d != correct_digit]
        check_digit = random.choice(invalid_choices)

    return partial + check_digit


class TestCreditCardValidator(unittest.TestCase):
    def test_valid_visa(self):
        for _ in range(20000):
            is_valid = random.choice([True, False])
            card = make_credit_card('4', 16, valid_check=is_valid)
            credit_card_validator(card)

    def test_mastercard(self):
        for _ in range(20000):
            if random.random() < 0.5:
                prefix = str(random.randint(50, 56))
            else:
                prefix = str(random.randint(2220, 2721))
            is_valid = random.choice([True, False])
            card = make_credit_card(prefix, 16, valid_check=is_valid)
            credit_card_validator(card)

    def test_valid_amex(self):
        for _ in range(20000):
            prefix = random.choice(['34', '37'])
            is_valid = random.choice([True, False])
            card = make_credit_card(prefix, 15, valid_check=is_valid)
            credit_card_validator(card)

    def test_random_combos(self):
        base = ''.join(random.choices('0123456789', k=9))
        small_card = base + checkdigit(base)
        credit_card_validator(small_card)

        base2 = ''.join(random.choices('0123456789', k=18))
        big_card = base2 + checkdigit(base2)
        credit_card_validator(big_card)

        for _ in range(20000):
            length = random.randint(2, 20)
            base = ''.join(random.choices('0123456789', k=length - 1))
            luhn = checkdigit(base)
            check = luhn if random.choice([True, False]) else random.choice(
                [d for d in '0123456789' if d != luhn]
            )
            credit_card_validator(base + check)


if __name__ == '__main__':
    unittest.main()
