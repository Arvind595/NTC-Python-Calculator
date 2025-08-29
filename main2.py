import math

def ntc_temperature(R_ntc, B, R25):
    """Calculate temperature (°C) from NTC resistance."""
    T_kelvin = 1 / ((1/298.15) + (1/B) * math.log(R_ntc / R25))
    return T_kelvin - 273.15

def ntc_resistance(T_celsius, B, R25):
    """Calculate resistance (Ω) of NTC at given temperature (°C)."""
    T_kelvin = T_celsius + 273.15
    return R25 * math.exp(B * ((1/T_kelvin) - (1/298.15)))

def optimal_series_resistor(T_min, T_max, B, R25):
    """Calculate optimal series resistor for ADC divider."""
    R_min = ntc_resistance(T_max, B, R25)  # resistance at hottest
    R_max = ntc_resistance(T_min, B, R25)  # resistance at coldest
    R1 = math.sqrt(R_min * R_max)
    return R1, R_min, R_max

def divider_voltage(R_ntc, R1, Vs):
    """Calculate voltage across NTC in divider."""
    return Vs * (R_ntc / (R1 + R_ntc))

def adc_code(Vout, Vs, bits=10):
    """Convert voltage to ADC code (integer)."""
    levels = (2**bits) - 1
    return round((Vout / Vs) * levels)

if __name__ == "__main__":
    print("=== NTC Thermistor Calculator with Voltage Divider and ADC ===")
    
    # Get fixed parameters
    B = float(input("Enter Beta value (B) in Kelvin: "))
    R25 = float(input("Enter resistance at 25°C (ohms): "))
    Vs = float(input("Enter ADC supply/reference voltage (V): ") or 5.0)
    bits = int(input("Enter ADC resolution in bits (default 10): ") or 10)
    
    while True:
        print("\nChoose an option:")
        print("1. Resistance → Temperature")
        print("2. Temperature → Resistance")
        print("3. Optimal series resistor (R1), ADC voltages & codes")
        print("4. Divider output at given resistance")
        print("5. Divider output at given temperature")
        print("q. Quit")
        
        choice = input("Enter choice: ").strip().lower()
        
        if choice == "q":
            print("Exiting...")
            break
        
        elif choice == "1":
            R_ntc = float(input("Enter measured NTC resistance (ohms): "))
            temperature = ntc_temperature(R_ntc, B, R25)
            print(f"Calculated Temperature: {temperature:.2f} °C")
        
        elif choice == "2":
            T_celsius = float(input("Enter temperature (°C): "))
            R_ntc = ntc_resistance(T_celsius, B, R25)
            print(f"Calculated Resistance: {R_ntc:.2f} Ω")
        
        elif choice == "3":
            Tmin = float(input("Enter minimum operating temperature (°C): "))
            Tmax = float(input("Enter maximum operating temperature (°C): "))
            R1, Rmin, Rmax = optimal_series_resistor(Tmin, Tmax, B, R25)
            
            Vmin = divider_voltage(Rmax, R1, Vs)
            Vmax = divider_voltage(Rmin, R1, Vs)
            ADCmin = adc_code(Vmin, Vs, bits)
            ADCmax = adc_code(Vmax, Vs, bits)
            
            print(f"\nAt Tmin = {Tmin}°C → R_NTC = {Rmax:.2f} Ω → Vout = {Vmin:.2f} V → ADC = {ADCmin}")
            print(f"At Tmax = {Tmax}°C → R_NTC = {Rmin:.2f} Ω → Vout = {Vmax:.2f} V → ADC = {ADCmax}")
            print(f"Recommended Series Resistor R1 = {R1:.2f} Ω")
        
        elif choice == "4":
            R1 = float(input("Enter series resistor R1 (ohms): "))
            R_ntc = float(input("Enter NTC resistance (ohms): "))
            Vout = divider_voltage(R_ntc, R1, Vs)
            ADC = adc_code(Vout, Vs, bits)
            print(f"Vout = {Vout:.2f} V → ADC = {ADC}")
        
        elif choice == "5":
            R1 = float(input("Enter series resistor R1 (ohms): "))
            T_celsius = float(input("Enter temperature (°C): "))
            R_ntc = ntc_resistance(T_celsius, B, R25)
            Vout = divider_voltage(R_ntc, R1, Vs)
            ADC = adc_code(Vout, Vs, bits)
            print(f"At {T_celsius:.2f} °C → R_NTC = {R_ntc:.2f} Ω → Vout = {Vout:.2f} V → ADC = {ADC}")
        
        else:
            print("Invalid choice, please select 1–5 or q.")
