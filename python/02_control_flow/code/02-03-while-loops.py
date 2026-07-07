"""Squid Game — countdown timer and game loop"""

import random

print("=== Red Light, Green Light Countdown ===")
countdown = 5
while countdown > 0:
    print(f"  {countdown}...")
    countdown -= 1
print("  GO!")

print("\n=== Guard Password Check ===")
password = ""
while password != "456":
    password = input("Enter the VIP code: ")
print("  Access granted.")

print("\n=== Marble Game ===")
marbles = 10
while marbles > 0:
    print(f"\n  You have {marbles} marbles.")
    bet = int(input("  Place your bet (1-3 marbles): "))
    if bet > marbles:
        print("  You don't have that many!")
        continue
    if random.choice([True, False]):
        marbles += bet
        print(f"  You won {bet} marbles!")
    else:
        marbles -= bet
        print(f"  You lost {bet} marbles.")

print("\n  Game over! You're out of marbles.")
