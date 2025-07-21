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

def make_credit_card(prefix, length):
    num_random_digits = length - len(prefix) - 1
    middle = ''.join(random.choice('0123456789') for _ in range(num_random_digits))
    partial_number = prefix + middle
    check_digit = calculate_check_digit(partial_number)
    return partial_number + check_digit

class TestCreditCardValidator(unittest.TestCase):

    def test_visa_cards(self):
        for _ in range(200):
            card = make_credit_card('4', 16)
            credit_card_validator(card)

    def test_mastercard_cards(self):
        prefixes = [str(i) for i in range(51, 56)] + [str(i) for i in range(2221, 2721)]
        for _ in range(200):
            prefix = random.choice(prefixes)
            card = make_credit_card(prefix, 16)
            credit_card_validator(card)

    def test_amex_cards(self):
        for _ in range(200):
            prefix = random.choice(['34', '37'])
            card = make_credit_card(prefix, 15)
            credit_card_validator(card)

if __name__ == '__main__':
    unittest.main()
