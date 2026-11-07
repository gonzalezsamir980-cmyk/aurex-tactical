def calcular_torque(masa, longitud):
    try:
        masa_kg = masa / 1000
        longitud_m = longitud / 100
        torque = masa_kg * longitud_m
        print(f"El torque necesario es: {torque} N*m")
        print(f"El torque necesario es: {torque * 100} kg*cm")
    except Exception as e:
        print(f"Error: {e}")

calcular_torque(2500, 35)