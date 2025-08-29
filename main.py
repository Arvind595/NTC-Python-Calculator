import math

def ntc_temperature(R_ntc, B, R25):
    """
    Calculate temperature (°C) from NTC resistance.
    """
    T_kelvin = 1 / ((1/298.15) + (1/B) * math.log(R_ntc / R25))
    return T_kelvin - 273.15

def ntc_resistance(T_celsius, B, R25):
    """
    Calculate resistance (ohms) of NTC at given temperature (°C).
    """
    T_kelvin = T_celsius + 273.15
    R_ntc = R25 * math.exp(B * ((1/T_kelvin) - (1/298.15)))
    return R_ntc

if __name__ == "__main__":
    print("=== NTC Thermistor Calculator ===")
    
    # Get fixed parameters once
    B = float(input("Enter Beta value (B) in Kelvin: "))
    R25 = float(input("Enter resistance at 25°C (ohms): "))
    
    while True:
        print("\nChoose an option:")
        print("1. Resistance → Temperature")
        print("2. Temperature → Resistance")
        print("q. Quit")
        
        choice = input("Enter choice: ").strip().lower()
        
        if choice == "q":
            print("Exiting...")
            break
        
        elif choice == "1":
            try:
                R_ntc = float(input("Enter measured NTC resistance (ohms): "))
                temperature = ntc_temperature(R_ntc, B, R25)
                print(f"Calculated Temperature: {temperature:.2f} °C")
            except ValueError:
                print("Invalid input.")
        
        elif choice == "2":
            try:
                T_celsius = float(input("Enter temperature (°C): "))
                R_ntc = ntc_resistance(T_celsius, B, R25)
                print(f"Calculated Resistance: {R_ntc:.2f} Ω")
            except ValueError:
                print("Invalid input.")
        
        else:
            print("Invalid choice, please select 1, 2, or q.")
