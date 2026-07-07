"""Recipe scaling — adjusting ingredient quantities with operators"""

original_flour = 2.0
original_sugar = 1.5
original_eggs = 3
original_butter = 0.5

scale_factor = 6 / 4

flour_needed = original_flour * scale_factor
sugar_needed = original_sugar * scale_factor
eggs_needed = original_eggs * scale_factor
butter_needed = original_butter * scale_factor

print(f"To serve 6, you need:")
print(f"  Flour: {flour_needed} cups")
print(f"  Sugar: {sugar_needed} cups")
print(f"  Eggs: {eggs_needed}")
print(f"  Butter: {butter_needed} cups")

total_eggs_needed = 15
dozens = total_eggs_needed // 12
loose_eggs = total_eggs_needed % 12
print(f"\n{total_eggs_needed} eggs = {dozens} dozen + {loose_eggs} loose")

print(f"\nNeed more than 2 cups flour? {flour_needed > 2.0}")

has_flour = flour_needed <= 5.0
has_sugar = sugar_needed <= 2.0
can_bake = has_flour and has_sugar
print(f"Can I bake? {can_bake}")
