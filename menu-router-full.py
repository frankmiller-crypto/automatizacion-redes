from netmiko import ConnectHandler
import time
from colorama import Fore, init
import os
from tqdm import tqdm

# Inicializar colorama
init(autoreset=True)

# Define los parámetros de conexión
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.161.156',  # Cambia esta IP a la de tu router
    'username': 'cisco',
    'password': 'cisco',
}

def mostrar_interfaces(connection):
    output = connection.send_command("show ip interface brief")
    print(f"\n{Fore.GREEN}Resultado de 'show ip interface brief':{Fore.RESET}")
    print(output)

def mostrar_tabla_enrutamiento(connection):
    output = connection.send_command("show ip route")
    print(f"\n{Fore.GREEN}Resultado de 'show ip route':{Fore.RESET}")
    print(output)

def realizar_backup(connection):
    output = connection.send_command("show running-config")
    # Solicitar la ruta y nombre del archivo donde guardar el backup
    filename = input(f"{Fore.YELLOW}Ingrese la ruta completa para guardar el backup (ejemplo: /path/to/backup_config.txt): {Fore.RESET}")
    
    # Verificar si la ruta existe
    if not os.path.isdir(os.path.dirname(filename)):
        print(f"{Fore.RED}ERROR: La ruta proporcionada no es válida.{Fore.RESET}")
        return

    try:
        with open(filename, "w") as file:
            file.write(output)
        print(f"{Fore.GREEN}Respaldo de la configuración guardado como {filename}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}ERROR: No se pudo guardar el respaldo. {e}{Fore.RESET}")

def cargar_config(connection):
    # Solicitar la ruta del archivo de configuración a cargar
    filename = input(f"{Fore.YELLOW}Ingrese la ruta completa del archivo de configuración a cargar (ejemplo: /path/to/backup_config.txt): {Fore.RESET}")
    
    # Verificar si el archivo existe
    if not os.path.isfile(filename):
        print(f"{Fore.RED}ERROR: El archivo de configuración no se encontró en la ruta proporcionada.{Fore.RESET}")
        return

    try:
        with open(filename, "r") as file:
            config_data = file.read()

        # Enviar configuración al router
        connection.send_config_set(config_data.splitlines())
        print(f"{Fore.GREEN}Configuración cargada desde {filename}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}ERROR: No se pudo cargar la configuración. {e}{Fore.RESET}")

def reiniciar_router(connection, tiempo_segundos):
    print(f"{Fore.YELLOW}Reinicio programado en {tiempo_segundos} segundos...\n")
    
    # Usamos tqdm para la barra de progreso
    for i in tqdm(range(tiempo_segundos, 0, -1), desc="Reiniciando el router", ncols=100, ascii=True):
        time.sleep(1)  # Espera de 1 segundo

    try:
        # Enviar el comando reload y esperar interacciones
        connection.send_command_timing("reload")
        # Esperar el mensaje de confirmación de guardado
        connection.send_command_timing("yes")
        print(f"\n{Fore.GREEN}Router reiniciado.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}ERROR: No se pudo reiniciar el router. {e}{Fore.RESET}")

def menu():
    # Establecer conexión con el router
    try:
        connection = ConnectHandler(**router)
        
        while True:
            print("\n--- Menú de opciones ---")
            print("1. Mostrar interfaces")
            print("2. Mostrar tabla de enrutamiento")
            print("3. Realizar un backup de la configuración")
            print("4. Cargar configuración de respaldo")
            print("5. Realizar un reinicio programado")
            print("6. Salir")
            
            opcion = input("Seleccione una opción (1-6): ")

            if opcion == '1':
                mostrar_interfaces(connection)
            elif opcion == '2':
                mostrar_tabla_enrutamiento(connection)
            elif opcion == '3':
                realizar_backup(connection)
            elif opcion == '4':
                cargar_config(connection)
            elif opcion == '5':
                try:
                    tiempo = int(input("¿En cuántos segundos desea que se reinicie el router? "))
                    reiniciar_router(connection, tiempo)
                except ValueError:
                    print(f"{Fore.RED}ERROR: Por favor, ingrese un número válido de segundos.{Fore.RESET}")
            elif opcion == '6':
                print(f"{Fore.GREEN}Saliendo del programa...{Fore.RESET}")
                break
            else:
                print(f"{Fore.RED}Opción no válida. Intente nuevamente.{Fore.RESET}")

        # Cerrar la conexión después de salir
        connection.disconnect()
    
    except Exception as e:
        print(f"{Fore.RED}ERROR: Hubo un error al conectarse al router: {e}{Fore.RESET}")

if __name__ == "__main__":
    menu()
