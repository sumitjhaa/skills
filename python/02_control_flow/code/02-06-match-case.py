"""Squid Game — game state machine and outcome classification"""

print("=== Squid Game Round Result ===")

def classify_outcome(outcome_code):
    match outcome_code:
        case 1:
            return "Player won the round"
        case 2:
            return "Player eliminated"
        case 3:
            return "Draw — both eliminated"
        case 4:
            return "Medical timeout"
        case _:
            return "Unknown outcome"

for code in [1, 4, 2, 99]:
    print(f"  Code {code}: {classify_outcome(code)}")

print("\n=== Performance Evaluation ===")

def evaluate_performance(kills, deaths, assists):
    score = kills * 10 + assists * 5 - deaths * 8
    match score:
        case _ if score > 50:
            return "Dominant performance!"
        case _ if score > 20:
            return "Solid performance"
        case _ if score > 0:
            return "Average performance"
        case _:
            return "Needs improvement"

print(f"  Score 55: {evaluate_performance(5, 0, 2)}")
print(f"  Score 25: {evaluate_performance(3, 2, 1)}")
print(f"  Score -5: {evaluate_performance(1, 4, 0)}")

print("\n=== Game State Machine ===")

def handle_command(command):
    match command:
        case ("start", level):
            return f"Starting game at level {level}"
        case ("pause",):
            return "Game paused"
        case ("resume",):
            return "Game resumed"
        case ("quit", reason):
            return f"Player quit: {reason}"
        case _:
            return "Unknown command"

print(f"  {handle_command(('start', 3))}")
print(f"  {handle_command(('pause',))}")
print(f"  {handle_command(('quit', 'too hard'))}")
