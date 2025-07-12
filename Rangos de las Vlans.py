while True:
    vlan_input = input("Ingrese el número de VLAN (o presione 'q' para salir): ")
    if vlan_input.lower() in ["q", "quit"]:
        print("Saliendo del programa de VLANs.")
        break

    if not vlan_input.isdigit():
        print("Se debe ingresar un número válido.")
        continue

    vlan = int(vlan_input)
    if 1 <= vlan <= 1005:
        print("La VLAN es de rango normal.")
    elif 1006 <= vlan <= 4094:
        print("<La VLAN es de rango extendido.")
    else:
        print("El Número de la VLAN esta fuera del rango válido.")
