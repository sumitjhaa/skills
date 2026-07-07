"""Matrix construct — checking if system components exist"""

print("=== Matrix System Check ===")

chosen_one = "Neo"
backup_code = ""
error_log = ["Agent Smith anomaly detected"]
null_ref = None
agent_count = 0
construct_version = 4.2

print(f"Chosen one exists: {bool(chosen_one)}")
print(f"Backup code exists: {bool(backup_code)}")
print(f"Errors logged: {bool(error_log)}")
print(f"Null reference: {bool(null_ref)}")
print(f"Agent count: {bool(agent_count)}")
print(f"Construct version: {bool(construct_version)}")

print("\n--- System Diagnosis ---")

if chosen_one:
    print("Chosen one identified — system online")
else:
    print("No chosen one — system idle")

if error_log:
    print(f"{len(error_log)} error(s) detected — check needed")
else:
    print("No errors — systems nominal")

if null_ref:
    print("Reference found")
else:
    print("Null reference — check connection")

if agent_count:
    print("Agents active — defensive mode")
else:
    print("No agents detected — safe")

if backup_code and chosen_one:
    print("\nFull recovery possible")
elif chosen_one or backup_code:
    print("\nPartial recovery — one component missing")
else:
    print("\nCritical failure — both missing")
