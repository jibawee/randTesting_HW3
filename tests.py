import unittest
import random
from credit_card_validator import credit_card_validator

def calculate_check_digit(number_without_check):
    total = 0
    reverse_digits = list(map(int, number_without_check[::-1]))

    for index in range(len(reverse_digits)):
        digit = reverse_digits[index]
        if index % 2 == 0:
            total += digit
        else:
            doubled = digit * 2
            if doubled < 10:
                total += doubled
            else:
                total += doubled - 9

    return str((10 - (total % 10)) % 10)

def make_credit_card(prefix, length):
    num_random_digits = length - len(prefix) - 1
    middle = ''
    for _ in range(num_random_digits):
        middle += random.choice('0123456789')

    partial_number = prefix + middle
    check_digit = calculate_check_digit(partial_number)
    full_number = partial_number + check_digit
    return full_number

class TestCreditCardValidator(unittest.TestCase):

    def test_visa_cards(self):
        for _ in range(200):
            # Visa prefix is just '4', length is 16
            card = make_credit_card('4', 16)
            credit_card_validator(card)

    def test_mastercard_cards(self):
        for _ in range(200):
            # MasterCard has two prefix ranges
            prefixes = []

            # 51 to 55
            for i in range(51, 56):
                prefixes.append(str(i))

            # 2221 to 2720
            for i in range(2221, 2721):
                prefixes.append(str(i))

            prefix = random.choice(prefixes)
            card = make_credit_card(prefix, 16)
            credit_card_validator(card)

    def test_amex_cards(self):
        for _ in range(200):
            # American Express uses 34 or 37
            prefix = random.choice(['34', '37'])
            card = make_credit_card(prefix, 15)
            credit_card_validator(card)

if __name__ == '__main__':
    unittest.main()