# Phase 02 Integration: Squid Game — combines conditionals, loops, loop control, nested loops

import random
import time


def red_light_green_light(players):
    print("\n=== Red Light, Green Light ===")
    survived = []
    for player in players:
        delay = random.uniform(0.5, 1.5)
        if delay > 1.0:
            print(f"  {player} moved — eliminated!")
            continue
        survived.append(player)
    return survived


def dalgona(players):
    print("\n=== Dalgona — Sugar Honeycomb ===")
    survivors = []
    for player in players:
        attempts = 0
        while attempts < 3:
            attempts += 1
            shape = random.choice(["triangle", "circle", "star", "umbrella"])
            precision = random.randint(1, 10)
            if precision >= 6:
                print(f"  {player} extracted the {shape} — safe!")
                survivors.append(player)
                break
            print(f"  {player} broke the {shape} on try {attempts}.")
        else:
            print(f"  {player} failed all attempts — eliminated!")
    return survivors


def tug_of_war(players):
    print("\n=== Tug of War ===")
    pairings = []
    for i in range(0, len(players) - 1, 2):
        pairings.append((players[i], players[i + 1]))
    if len(players) % 2:
        pairings.append((players[-1], None))
    survivors = []
    for p1, p2 in pairings:
        if p2 is None:
            survivors.append(p1)
            continue
        strength1 = random.randint(1, 100)
        strength2 = random.randint(1, 100)
        if strength1 > strength2:
            print(f"  {p1} beats {p2} — advances!")
            survivors.append(p1)
        elif strength2 > strength1:
            print(f"  {p2} beats {p1} — advances!")
            survivors.append(p2)
        else:
            print(f"  {p1} and {p2} draw — both eliminated!")
    return survivors


def marbles(players):
    print("\n=== Marbles ===")
    survivors = []
    for player in players:
        marbles_count = random.randint(1, 20)
        guess = random.randint(1, 3)
        match guess:
            case 1 if marbles_count > 10:
                print(f"  {player} guessed odd and had {marbles_count} marbles — safe!")
                survivors.append(player)
            case 2 if marbles_count <= 10:
                print(f"  {player} guessed even and had {marbles_count} marbles — safe!")
                survivors.append(player)
            case 3:
                print(f"  {player} tried to cheat — eliminated!")
            case _:
                print(f"  {player} guessed wrong — eliminated!")
    return survivors


def squid_game(players):
    print("\n=== Final: Squid Game ===")
    survivors = []
    for player in players:
        attack = random.randint(1, 5)
        defense = random.randint(1, 5)
        if attack > defense:
            print(f"  {player} attacks ({attack} > {defense}) — advances!")
            survivors.append(player)
        elif attack == defense:
            print(f"  {player} stalemate — eliminated!")
        else:
            print(f"  {player} fails to break through — eliminated!")
    return survivors


def main():
    print("=" * 45)
    print("  SQUID GAME — ELIMINATION SYSTEM")
    print("=" * 45)

    players = [f"Player_{i}" for i in range(1, 17)]
    print(f"\nStarting with {len(players)} players.\n")

    rounds = [
        ("Red Light, Green Light", red_light_green_light),
        ("Dalgona", dalgona),
        ("Tug of War", tug_of_war),
        ("Marbles", marbles),
        ("Squid Game", squid_game),
    ]

    for name, game_func in rounds:
        input(f"Press Enter to start {name}...")
        time.sleep(0.5)
        players = game_func(players)
        print(f"  Survivors: {len(players)} — {players}")
        if len(players) <= 1:
            break

    if players:
        print(f"\n{'=' * 45}")
        print(f"  WINNER: {players[0]}!")
        print(f"{'=' * 45}")
    else:
        print("\nNo winner — all players eliminated.")


if __name__ == "__main__":
    main()
