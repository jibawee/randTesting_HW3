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
        for _ in range(random.randint(500, 2000)):
            is_valid = random.choice([True, False])
            length = random.choice([13, 16, 19])
            card = make_credit_card('4', length, valid_check=is_valid)
            credit_card_validator(card)

    def test_mastercard(self):
        for _ in range(random.randint(500, 2000)):
            if random.random() < 0.5:
                prefix = str(random.randint(51, 55))
            else:
                prefix = str(random.randint(2221, 2720))
            is_valid = random.choice([True, False])
            length = random.choice([16, 17, 18, 19])
            card = make_credit_card(prefix, length, valid_check=is_valid)
            credit_card_validator(card)

    def test_amex(self):
        for _ in range(random.randint(500, 2000)):
            prefix = random.choice(['34', '37'])
            is_valid = random.choice([True, False])
            length = random.choice([15, 16, 17])
            card = make_credit_card(prefix, length, valid_check=is_valid)
            credit_card_validator(card)

    def test_mixed_valid_ranges(self):
        for _ in range(random.randint(500, 2000)):
            issuer = random.choice(['visa', 'mc', 'amex'])
            is_valid = random.choice([True, False])
            if issuer == 'visa':
                length = random.choice([13, 16, 19])
                card = make_credit_card('4', length, valid_check=is_valid)
            elif issuer == 'mc':
                prefix = str(random.choice(
                    list(range(51, 56)) + list(range(2221, 2721))
                ))
                length = random.choice([16, 17, 18, 19])
                card = make_credit_card(prefix, length, valid_check=is_valid)
            else:
                prefix = random.choice(['34', '37'])
                length = random.choice([15, 16, 17])
                card = make_credit_card(prefix, length, valid_check=is_valid)
            credit_card_validator(card)

    def test_edge_case_lengths(self):
        all_prefixes = (
            ['4'] +
            [str(i) for i in range(51, 56)] +
            [str(i) for i in range(2221, 2721)] +
            ['34', '37']
        )
        for _ in range(random.randint(500, 2000)):
            prefix = random.choice(all_prefixes)
            length = random.randint(10, 19)
            is_valid = random.choice([True, False])
            if len(prefix) < length - 1:
                card = make_credit_card(prefix, length, valid_check=is_valid)
                credit_card_validator(card)


if __name__ == '__main__':
    unittest.main()