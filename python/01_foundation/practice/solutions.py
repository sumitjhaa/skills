"""Solutions for Phase 01 practice exercises"""

# Exercise 1: Cricket Scorecard
def cricket_scorecard():
    name = "Virat Kohli"
    runs = 82
    balls = 53
    is_out = True
    strike_rate = (runs / balls) * 100
    print(f"Batsman: {name}")
    print(f"Runs: {runs}")
    print(f"Balls: {balls}")
    print(f"Strike Rate: {strike_rate:.2f}")
    print(f"Out: {'Yes' if is_out else 'No'}")

# Exercise 2: Pizza Order Calculator
def pizza_calculator():
    pizzas = int(input("Number of pizzas: "))
    slices_per = int(input("Slices per pizza: "))
    total = pizzas * slices_per
    per_person = total // 8
    leftover = total % 8
    print(f"Total slices: {total}")
    print(f"Slices per person (8 people): {per_person}")
    print(f"Leftover slices: {leftover}")

# Exercise 3: Character Creation
def character_creation():
    name = input("Enter character name: ")
    char_class = input("Enter class: ")
    level = int(input("Enter starting level: "))
    hp = level * 25
    mana = level * 8 + 1
    print("=== CHARACTER SHEET ===")
    print(f"Name: {name}")
    print(f"Class: {char_class}")
    print(f"Level: {level}")
    print(f"HP: {hp}")
    print(f"Mana: {mana}")

# Exercise 4: Temperature Alert
def temperature_alert():
    celsius = float(input("Enter temperature in Celsius: "))
    fahrenheit = celsius * 9 / 5 + 32
    print(f"{celsius}°C = {fahrenheit}°F")
    if celsius > 30:
        print("Heat warning!")
    elif celsius < 5:
        print("Freeze warning!")
    else:
        print("Temperature normal.")

# Exercise 5: Type Identification
def type_identification():
    items = [42, 0.0, "hello", False]
    for item in items:
        kind = type(item).__name__
        truthy = "Truthy" if bool(item) else "Falsy"
        print(f"Value: {item} → Type: {kind} → {truthy}")

# Exercise 6: Grade Calculator
def grade_calculator():
    s1 = float(input("Test 1: "))
    s2 = float(input("Test 2: "))
    s3 = float(input("Test 3: "))
    avg = (s1 + s2 + s3) / 3
    print(f"Average: {avg}")
    print(f"Status: {'Passed' if avg >= 60 else 'Failed'}")

# Exercise 7: Swap & Compare
def swap_compare():
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    print(f"Before: a={a}, b={b}")
    a, b = b, a
    print(f"After: a={a}, b={b}")
    print(f"a > b? {a > b}")

# Exercise 8: Menu Price Calculator
def menu_price():
    burgers = int(input("How many burgers? "))
    fries = int(input("How many fries? "))
    drinks = int(input("How many drinks? "))
    subtotal = burgers * 8.50 + fries * 3.00 + drinks * 2.50
    tax = subtotal * 0.08
    total = subtotal + tax
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax (8%): ${tax:.2f}")
    print(f"Total: ${total:.2f}")

if __name__ == "__main__":
    print("=== Cricket Scorecard ===")
    cricket_scorecard()
    print("\n=== Pizza Calculator ===")
    pizza_calculator()
    print("\n=== Character Creation ===")
    character_creation()
    print("\n=== Temperature Alert ===")
    temperature_alert()
    print("\n=== Type Identification ===")
    type_identification()
    print("\n=== Grade Calculator ===")
    grade_calculator()
    print("\n=== Swap & Compare ===")
    swap_compare()
    print("\n=== Menu Price Calculator ===")
    menu_price()
