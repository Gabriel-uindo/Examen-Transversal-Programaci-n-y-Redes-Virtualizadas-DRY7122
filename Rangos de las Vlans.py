while True:
    vlan_input = input("Ingrese el número de VLAN (o presione 'q' para salir): ")
    if vlan_input.lower() in ["q", "quit"]:
        print("Saliendo del programa de VLANs.")
        break

    if not vlan_input.isdigit():
        print("⚠️ Debe ingresar un número válido.")
        continue

    vlan = int(vlan_input)
    if 1 <= vlan <= 1005:
        print("✅ VLAN en rango normal.")
    elif 1006 <= vlan <= 4094:
        print("✅ VLAN en rango extendido.")
    else:
        print("⚠️ Número de VLAN fuera de rango válido.")
