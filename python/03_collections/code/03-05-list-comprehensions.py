"""Weather data analysis — list comprehensions for temperature processing"""

temps = [23.5, 18.0, 35.2, 28.8, 15.1, 32.7, 22.4, 30.0, 12.3, 27.6]

print("=== Weather Analysis ===")

fahrenheit = [(t * 9 / 5 + 32) for t in temps]
print(f"Temps in °F: {[round(f, 1) for f in fahrenheit]}")

hot_days = [t for t in temps if t > 30]
print(f"\nHot days (>30°C): {hot_days}")

labels = ["Hot" if t > 30 else "Warm" if t > 20 else "Cool" for t in temps]
for i, (temp, label) in enumerate(zip(temps, labels), 1):
    print(f"  Day {i}: {temp}°C — {label}")

cities = ["london", "paris", "new york", "tokyo"]
capitalized = [city.title() for city in cities]
print(f"\nCities: {capitalized}")

long_cities = [city.title() for city in cities if len(city) > 5]
print(f"Long city names: {long_cities}")

grid = [(x, y) for x in range(3) for y in range(3)]
print(f"\nCoordinate grid: {grid}")

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Flattened matrix: {flattened}")
