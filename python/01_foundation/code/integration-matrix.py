"""
Phase 01 Integration: The Matrix — combines variables, types, operators, I/O, casting

Neo's training program: enter the Matrix, check stats, make choices, see outcomes.
"""

import sys
import textwrap

TITLE = "The Matrix — Training Program"
VERSION = 1.0

def main():
    print("=" * 50)
    print(f"  {TITLE}")
    print("=" * 50)

    name = input("\nEnter your name, Neo: ").strip()
    if not name:
        name = "Neo"

    print(f"\nWelcome to the Matrix, {name}.")
    print("The simulation is unstable. We need your help.")

    age = int(input("How old are you? "))
    level = float(input("Enter your current skill level (0.0 - 10.0): "))

    base_power = age * level
    print(f"\n[Analyzing...] Base power score: {base_power}")
    print(f"[Type:] {type(base_power).__name__}")

    is_chosen = base_power > 50.0
    if is_chosen:
        print(f"[Status:] You are The One, {name}.")
    else:
        print(f"[Status:] Not yet chosen, {name}. Train harder.")

    print(f"\n--- Augmented Training ---")
    level += 1.5
    age += 1
    base_power = age * level
    print(f"After training: level={level}, age={age}, power={base_power}")

    print("\n--- Matrix Combat Simulator ---")
    enemy_count = int(input("How many Agents are after you? "))
    bullets = 50
    shots_per_agent = 3
    total_shots_needed = enemy_count * shots_per_agent

    has_enough_bullets = bullets >= total_shots_needed
    has_skill = level > 5.0
    can_survive = has_enough_bullets and has_skill

    print(f"\nBullets available: {bullets}")
    print(f"Shots needed: {total_shots_needed}")
    print(f"Enough bullets? {has_enough_bullets}")
    print(f"Skilled enough? {has_skill}")
    print(f"Survival prediction: {can_survive}")

    print(f"\n--- Dodge This ---")
    speed = float(input("Enter your reaction speed (ms): "))
    can_dodge = speed < 150.0
    bullet_time = 100.0 if can_dodge else 300.0
    print(f"Bullet-time activated: {can_dodge}")
    print(f"Perceived time dilation: {bullet_time}ms")

    print(f"\n--- Final Assessment ---")
    stats = {
        "name": name,
        "age": age,
        "level": level,
        "power": base_power,
        "chosen": is_chosen,
        "survive": can_survive,
        "dodge": can_dodge,
    }

    print(f"\n{'-' * 40}")
    print(f"{'Stat':<20} {'Value':<10} {'Truthy?'}")
    print(f"{'-' * 40}")
    for key, value in stats.items():
        print(f"{key:<20} {str(value):<10} {bool(value)}")

    print(f"\n{'*' * 50}")
    print(f"  Matrix simulation complete, {name}.")
    outcome = can_survive and can_dodge
    if outcome:
        print(f"  You are ready. The prophecy is real.")
    else:
        print(f"  Keep training. The Matrix hasn't seen the last of you.")
    print(f"{'*' * 50}")

    exit_choice = input("\n[Enter 'exit' to leave the Matrix]: ")
    if exit_choice.strip().lower() == "exit":
        print("See you on the other side...")
    else:
        print(f"There is no escape, {name}.")

if __name__ == "__main__":
    main()
