#!/usr/bin/env python3
print("Hello, World!")
print("Starting the program...")
def meters_to_feet(meters: float) -> float:
    return meters * 3.280839895


def feet_to_meters(feet: float) -> float:
    return feet / 3.280839895


def kilograms_to_pounds(kg: float) -> float:
    return kg * 2.2046226218


def pounds_to_kilograms(lb: float) -> float:
    return lb / 2.2046226218


def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9 / 5) + 32


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


def prompt_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a numeric value.")


def main() -> None:
    menu = """
Metric ↔ Imperial Converter
---------------------------
1) Meters → Feet
2) Feet → Meters
3) Kilograms → Pounds
4) Pounds → Kilograms
5) Celsius → Fahrenheit
6) Fahrenheit → Celsius
0) Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (0-6): ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        if choice == "1":
            value = prompt_float("Enter meters: ")
            result = meters_to_feet(value)
            print(f"{value} m = {result:.3f} ft\n")
        elif choice == "2":
            value = prompt_float("Enter feet: ")
            result = feet_to_meters(value)
            print(f"{value} ft = {result:.3f} m\n")
        elif choice == "3":
            value = prompt_float("Enter kilograms: ")
            result = kilograms_to_pounds(value)
            print(f"{value} kg = {result:.3f} lb\n")
        elif choice == "4":
            value = prompt_float("Enter pounds: ")
            result = pounds_to_kilograms(value)
            print(f"{value} lb = {result:.3f} kg\n")
        elif choice == "5":
            value = prompt_float("Enter °C: ")
            result = celsius_to_fahrenheit(value)
            print(f"{value} °C = {result:.3f} °F\n")
        elif choice == "6":
            value = prompt_float("Enter °F: ")
            result = fahrenheit_to_celsius(value)
            print(f"{value} °F = {result:.3f} °C\n")
        else:
            print("Invalid choice. Please select 0–6.\n")


if __name__ == "__main__":
    main()

