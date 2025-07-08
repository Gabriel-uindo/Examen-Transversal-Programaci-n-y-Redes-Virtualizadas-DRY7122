from ncclient import manager

router = {
    'host': '192.168.1.5', 
    'port': 830,
    'username': 'cisco',
    'password': 'cisco123!',
    'hostkey_verify': False
}

netconf_payload = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>Apellido1-Apellido2</hostname>
        <interface>
            <Loopback>
                <name>11</name>
                <ip>
                    <address>
                        <primary>
                            <address>11.11.11.11</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

with manager.connect(**router) as m:
    print("Conectado al router NETCONF")
    response = m.edit_config(target="running", config=netconf_payload)
    print("Respuesta del router:")
    print(response)

print("✅ Configuración enviada exitosamente.")
