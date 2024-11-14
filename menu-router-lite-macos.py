from netmiko import ConnectHandler
import os
# Prueba de git
# Define los parámetros de conexión
router = {
    'device_type': 'cisco_ios',
    'ip': '172.16.173.141',  # Cambia esta IP a la de tu router
    'username': 'cisco',
    'password': 'cisco',
}

def obtener_hostname(connection):
    # Obtener el hostname del router
    output = connection.send_command("show run | include hostname")
    hostname = output.split()[-1]
    return hostname

def mostrar_interfaces(connection):
    output = connection.send_command("show ip interface brief")
    print("\nResultado de 'show ip interface brief':")
    print(output)

def mostrar_tabla_enrutamiento(connection):
    output = connection.send_command("show ip route")
    print("\nResultado de 'show ip route':")
    print(output)

def realizar_backup(connection):
    output = connection.send_command("show running-config")
    
    # Obtener el hostname del router para usarlo en el nombre del archivo
    hostname = obtener_hostname(connection)
    
    # Crear la carpeta de backups si no existe
    backup_folder = os.path.join(os.getcwd(), 'backups-config-file')
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # Definir el nombre del archivo de backup
    filename = os.path.join(backup_folder, f"{hostname}-running-config.txt")
    
    try:
        with open(filename, "w") as file:
            file.write(output)
        print(f"Respaldo de la configuración guardado como {filename}")
    except Exception as e:
        print(f"ERROR: No se pudo guardar el respaldo. {e}")

def mostrar_usuarios(connection):
    output = connection.send_command("show users")
    print("\nEstos son los usuarios conectados de manera remota:':")
    print(output)

def menu():
    # Establecer conexión con el router
    try:
        connection = ConnectHandler(**router)
        
        while True:
            print("\n--- Menú ---")
            print("1. Mostrar interfaces")
            print("2. Mostrar tabla de enrutamiento")
            print("3. Realizar un backup de la configuración")
            print("4. Mostrar usuarios conectados de manera rmeota")
            print("5. Salir")
            
            opcion = input("Seleccione una opción (1-5): ")

            if opcion == '1':
                mostrar_interfaces(connection)
            elif opcion == '2':
                mostrar_tabla_enrutamiento(connection)
            elif opcion == '3':
                realizar_backup(connection)
            elif opcion == '4':
                mostrar_usuarios(connection)
            elif opcion == '5':
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

        # Cerrar la conexión después de salir
        connection.disconnect()
    
    except Exception as e:
        print(f"ERROR: No se pudo conectar al router: {e}")

if __name__ == "__main__":
    menu()
