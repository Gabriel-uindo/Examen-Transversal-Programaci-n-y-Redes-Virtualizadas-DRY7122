from netmiko import ConnectHandler

# ==========================
# DATOS DE CONEXIÓN
# ==========================
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.5',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': '',  # si usas enable, pon aquí la enable password
}

# ==========================
# CONECTAR
# ==========================
net_connect = ConnectHandler(**router)
print("✅ Conectado al router mediante SSH")

# ==========================
# CONFIGURAR EIGRP IPv4 e IPv6
# ==========================
eigrp_config = [
    'router eigrp MiAS',
    'address-family ipv4 unicast autonomous-system 1',
    'network 192.168.0.0 0.0.0.255',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
    'exit-address-family',
    'address-family ipv6 unicast autonomous-system 1',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
    'exit-address-family'
]

output_config = net_connect.send_config_set(eigrp_config)
print("✅ Configuración EIGRP enviada")
print(output_config)

# ==========================
# EJECUTAR COMANDOS SHOW
# ==========================
print("\n==============================")
print("🔍 show ip interface brief")
print("==============================")
print(net_connect.send_command("show ip interface brief"))

print("\n==============================")
print("🔍 show running-config | section eigrp")
print("==============================")
print(net_connect.send_command("show running-config | section eigrp"))

print("\n==============================")
print("🔍 show version")
print("==============================")
print(net_connect.send_command("show version"))

net_connect.disconnect()
print("✅ Conexión cerrada.")
