from prime import is_prime

numbers = [1, 2, 13, 15, 97, 100]

for number in numbers:
    print(f"{number}: {is_prime(number)}")
