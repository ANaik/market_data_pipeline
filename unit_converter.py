#!/usr/bin/env python3

"""
Simple command-line converter between metric and imperial measurements.

Supported conversions:
- Length: meters ⟷ feet, kilometers ⟷ miles, centimeters ⟷ inches
- Weight: kilograms ⟷ pounds, grams ⟷ ounces
- Temperature: Celsius ⟷ Fahrenheit
"""

from __future__ import annotations


def meters_to_feet(meters: float) -> float:
    return meters * 3.280839895


def feet_to_meters(feet: float) -> float:
    return feet / 3.280839895


def kilometers_to_miles(km: float) -> float:
    return km * 0.621371192


def miles_to_kilometers(miles: float) -> float:
    return miles / 0.621371192


def centimeters_to_inches(cm: float) -> float:
    return cm * 0.3937007874


def inches_to_centimeters(inches: float) -> float:
    return inches / 0.3937007874


def kilograms_to_pounds(kg: float) -> float:
    return kg * 2.2046226218


def pounds_to_kilograms(lb: float) -> float:
    return lb / 2.2046226218


def grams_to_ounces(g: float) -> float:
    return g * 0.03527396195


def ounces_to_grams(oz: float) -> float:
    return oz / 0.03527396195


def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9.0 / 5.0) + 32.0


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0


def _get_float(prompt: str) -> float:
    """Read a float from stdin, reprompting on invalid input."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a numeric value.")


def _length_menu() -> None:
    print("\nLength conversions:")
    print(" 1) meters -> feet")
    print(" 2) feet -> meters")
    print(" 3) kilometers -> miles")
    print(" 4) miles -> kilometers")
    print(" 5) centimeters -> inches")
    print(" 6) inches -> centimeters")

    choice = input("Choose an option (1-6): ").strip()

    if choice == "1":
        value = _get_float("Enter meters: ")
        result = meters_to_feet(value)
        print(f"{value} m = {result:.4f} ft")
    elif choice == "2":
        value = _get_float("Enter feet: ")
        result = feet_to_meters(value)
        print(f"{value} ft = {result:.4f} m")
    elif choice == "3":
        value = _get_float("Enter kilometers: ")
        result = kilometers_to_miles(value)
        print(f"{value} km = {result:.4f} mi")
    elif choice == "4":
        value = _get_float("Enter miles: ")
        result = miles_to_kilometers(value)
        print(f"{value} mi = {result:.4f} km")
    elif choice == "5":
        value = _get_float("Enter centimeters: ")
        result = centimeters_to_inches(value)
        print(f"{value} cm = {result:.4f} in")
    elif choice == "6":
        value = _get_float("Enter inches: ")
        result = inches_to_centimeters(value)
        print(f"{value} in = {result:.4f} cm")
    else:
        print("Invalid choice.")


def _weight_menu() -> None:
    print("\nWeight conversions:")
    print(" 1) kilograms -> pounds")
    print(" 2) pounds -> kilograms")
    print(" 3) grams -> ounces")
    print(" 4) ounces -> grams")

    choice = input("Choose an option (1-4): ").strip()

    if choice == "1":
        value = _get_float("Enter kilograms: ")
        result = kilograms_to_pounds(value)
        print(f"{value} kg = {result:.4f} lb")
    elif choice == "2":
        value = _get_float("Enter pounds: ")
        result = pounds_to_kilograms(value)
        print(f"{value} lb = {result:.4f} kg")
    elif choice == "3":
        value = _get_float("Enter grams: ")
        result = grams_to_ounces(value)
        print(f"{value} g = {result:.4f} oz")
    elif choice == "4":
        value = _get_float("Enter ounces: ")
        result = ounces_to_grams(value)
        print(f"{value} oz = {result:.4f} g")
    else:
        print("Invalid choice.")


def _temperature_menu() -> None:
    print("\nTemperature conversions:")
    print(" 1) Celsius -> Fahrenheit")
    print(" 2) Fahrenheit -> Celsius")

    choice = input("Choose an option (1-2): ").strip()

    if choice == "1":
        value = _get_float("Enter Celsius: ")
        result = celsius_to_fahrenheit(value)
        print(f"{value} °C = {result:.2f} °F")
    elif choice == "2":
        value = _get_float("Enter Fahrenheit: ")
        result = fahrenheit_to_celsius(value)
        print(f"{value} °F = {result:.2f} °C")
    else:
        print("Invalid choice.")


def main() -> None:
    while True:
        print("\nMetric ↔ Imperial Converter")
        print("---------------------------")
        print(" 1) Length")
        print(" 2) Weight")
        print(" 3) Temperature")
        print(" 4) Quit")

        choice = input("Choose a category (1-4): ").strip()

        if choice == "1":
            _length_menu()
        elif choice == "2":
            _weight_menu()
        elif choice == "3":
            _temperature_menu()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please pick 1-4.")


if __name__ == "__main__":
    main()

