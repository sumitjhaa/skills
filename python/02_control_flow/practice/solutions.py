"""Solutions for Phase 02 practice exercises"""

# Exercise 1: Squid Game Eligibility
def squid_eligibility():
    age = int(input("Enter your age: "))
    debt = float(input("Enter your debt (in millions): "))
    if age < 18:
        print("Too young.")
    elif age >= 18 and debt > 10:
        print("Eligible for Squid Game.")
    else:
        print("Debt too low — not eligible.")

# Exercise 2: FizzBuzz
def fizzbuzz():
    for i in range(1, 51):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

# Exercise 3: Sum Until Zero
def sum_until_zero():
    total = 0
    while True:
        num = int(input("Enter a number (0 to stop): "))
        if num == 0:
            break
        total += num
    print(f"Total: {total}")

# Exercise 4: Prime Checker
def prime_checker():
    n = int(input("Enter a number: "))
    if n < 2:
        print(f"{n} is not prime.")
        return
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            print(f"{n} is not prime.")
            break
    else:
        print(f"{n} is prime.")

# Exercise 5: Multiplication Table
def multiplication_table():
    for i in range(1, 11):
        for j in range(1, 11):
            print(f"{i * j:4}", end=" ")
        print()

# Exercise 6: Password Validator
def password_validator():
    while True:
        pw = input("Create a password: ")
        if len(pw) < 8:
            print("Too short — need at least 8 characters.")
            continue
        if not any(ch.isdigit() for ch in pw):
            print("Need at least one digit.")
            continue
        if not any(ch.isupper() for ch in pw):
            print("Need at least one uppercase letter.")
            continue
        print("Password accepted!")
        break

# Exercise 7: Number Pyramid
def number_pyramid():
    n = 5
    for i in range(1, n + 1):
        for _ in range(n - i):
            print(" ", end=" ")
        for j in range(1, i + 1):
            print(j, end=" ")
        print()

# Exercise 8: HTTP Status Classifier
def http_status_classifier():
    code = int(input("Enter HTTP status code: "))
    match code:
        case _ if 100 <= code < 200:
            print("Informational")
        case _ if 200 <= code < 300:
            print("Success")
        case _ if 300 <= code < 400:
            print("Redirection")
        case _ if 400 <= code < 500:
            print("Client Error")
        case _ if 500 <= code < 600:
            print("Server Error")
        case _:
            print("Unknown")

if __name__ == "__main__":
    print("Run individual functions to test.")
    print("Call: squid_eligibility(), fizzbuzz(), sum_until_zero(), etc.")
