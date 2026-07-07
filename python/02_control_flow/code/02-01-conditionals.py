"""Squid Game — Red Light, Green Light elimination"""

speed = 3.2
reaction_ms = 450

if speed > 5.0:
    print("Sprinting! Fast player.")
elif speed > 3.0:
    print("Moving at a steady jog.")
elif speed > 1.0:
    print("Slow walk — risky!")
else:
    print("Barely moving — might not cross in time.")

print(f"\nRed Light! Reaction time: {reaction_ms}ms")

if reaction_ms < 200:
    print("Froze instantly — safe!")
elif reaction_ms < 500:
    print("Hesitated — almost eliminated!")
else:
    print("Too slow! Eliminated.")

status = "Survived" if reaction_ms < 500 else "Eliminated"
print(f"\nResult: {status}")

if speed > 2.0:
    if reaction_ms < 300:
        print("Elite player — fast and quick reflexes!")
    else:
        print("Fast but slow reactions — dangerous combo.")
