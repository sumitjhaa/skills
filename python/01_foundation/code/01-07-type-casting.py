"""Weather app — converting temperature strings for comparison"""

print("=== Weather Station ===")

temp_string = input("Enter current temperature (°C): ")
humidity_string = input("Enter humidity percentage: ")

temperature = float(temp_string)
humidity = int(humidity_string)

print(f"\nCurrent temperature: {temperature}°C")
print(f"Humidity: {humidity}%")

if temperature > 30:
    print("Hot day — stay hydrated!")
elif temperature > 20:
    print("Pleasant weather — enjoy the day!")
else:
    print("Cool — bring a jacket!")

if humidity > 70:
    print("High humidity — might rain!")

report = "Temp: " + str(temperature) + "°C | Humidity: " + str(humidity) + "%"
print(f"\nWeather Report: {report}")

raw_value = "5.5"
try:
    safe_value = int(float(raw_value))
    print(f"\nSafe conversion of '{raw_value}': {safe_value}")
except ValueError:
    print(f"\nCould not convert '{raw_value}' to a number.")
