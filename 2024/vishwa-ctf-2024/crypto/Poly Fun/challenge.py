import numpy as np
import random

polyc = [4,3,7]
poly = np.poly1d(polyc)


def generate_random_number():
    while True:
        num = random.randint(100, 999)
        first_digit = num // 100
        last_digit = num % 10
        if abs(first_digit - last_digit) > 1:
            return num


def generate_random_number_again():
    while True:
        num = random.randint(1000, 9999)
        if num % 1111 != 0:
            return num


def transform(num):
    number = random.randint(1, 100000)
    org = number
    number *= 2
    number += 15
    number *= 3
    number += 33
    number /= 6
    number -= org
    if number == 13:
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        number = num1 * 2
        number += 5
        number *= 5
        number += num2
        number -= 25
        if int(number / 10) == num1 and number % 10 == num2:
            number = generate_random_number()
            num1 = int(''.join(sorted(str(number), reverse=True)))
            num2 = int(''.join(sorted(str(number))))
            diff = abs(num1 - num2)
            rev_diff = int(str(diff)[::-1])
            number = diff + rev_diff
            if number == 1088:
                org = num
                num *= 2
                num /= 3
                num += 5
                num *= 4
                num -= 9
                num -= org
                return num
            else:
                number = generate_random_number_again()
                i = 0
                while number != 6174:
                    digits = [int(d) for d in str(number)]
                    digits.sort()
                    smallest = int(''.join(map(str, digits)))
                    digits.reverse()
                    largest = int(''.join(map(str, digits)))
                    number = largest - smallest
                    i += 1

                if i <= 7:
                    org = num
                    num *= 2
                    num += 7
                    num += 5
                    num -= 12
                    num -= org
                    num += 4
                    num *= 2
                    num -= 8
                    num -= org
                    return num
                else:
                    org = num
                    num **= 4
                    num /= 9
                    num += 55
                    num *= 6
                    num += 5
                    num -= 23
                    num -= org
                    return num
        else:
            org = num
            num *= 10
            num += 12
            num **= 3
            num -= 6
            num += 5
            num -= org
            return num
    else:
        org = num
        num += 5
        num -= 10
        num *= 2
        num += 12
        num -= 20
        num -= org
        return num


def encrypt(p,key):
    return ''.join(chr(p(transform(i))) for i in key)


key = open('key.txt', 'rb').read()
enc = encrypt(poly,key)
print(enc)
