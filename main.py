import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os
import shutil
import subprocess
import ctypes
import sys
import socket

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(sys.argv), None, 1
        )
        sys.exit()

def delete_file():
    filepath = filedialog.askopenfilename(title="Seleccione un archivo para borrar")
    if filepath:
        try:
            os.remove(filepath)
            messagebox.showinfo("Éxito", f"Archivo '{filepath}' borrado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar el archivo: {e}")

def delete_folder():
    folderpath = filedialog.askdirectory(title="Seleccione una carpeta para borrar")
    if folderpath:
        try:
            shutil.rmtree(folderpath)
            messagebox.showinfo("Éxito", f"Carpeta '{folderpath}' y su contenido borrados exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar la carpeta: {e}")

def get_mac_address():
    ip_address = simpledialog.askstring("Obtener MAC", "Ingrese la dirección IP:")
    if ip_address:
        try:
            subprocess.run(["ping", "-n", "1", ip_address], check=True)
            arp_output = subprocess.check_output(["arp", "-a", ip_address], stderr=subprocess.STDOUT)
            arp_output = arp_output.decode('latin1')
            lines = arp_output.split('\n')
            for line in lines:
                if ip_address in line:
                    mac_address = line.split()[1]
                    messagebox.showinfo("Dirección MAC", f"La dirección MAC de {ip_address} es {mac_address}")
                    return mac_address
            messagebox.showerror("Error", "No se pudo encontrar la dirección MAC.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo obtener la dirección MAC: {e}")
        except IndexError:
            messagebox.showerror("Error", "No se pudo encontrar la dirección MAC en la salida ARP.")
        except UnicodeDecodeError:
            messagebox.showerror("Error", "No se pudo decodificar la salida del comando ARP.")

def show_system_info():
    try:
        system_name = subprocess.check_output("wmic computersystem get name", shell=True).decode().strip().split('\n')[1].strip()
        serial_number = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().strip().split('\n')[1].strip()
        ip_address = socket.gethostbyname(socket.gethostname())
        return system_name, serial_number, ip_address
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la información del sistema: {e}")
        return None, None, None

def save_system_info(system_name, serial_number, ip_address):
    try:
        with open(f"{system_name}_info_equipo.txt", "w") as f:
            f.write(f"Nombre del Sistema: {system_name}\n")
            f.write(f"Número de Serie: {serial_number}\n")
            f.write(f"Dirección IP: {ip_address}\n")
        messagebox.showinfo("Éxito", f"Información guardada en '{system_name}_info_equipo.txt'.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la información: {e}")

def show_info_message():
    system_name, serial_number, ip_address = show_system_info()
    if system_name and serial_number and ip_address:
        message = f"Nombre del Sistema: {system_name}\nNúmero de Serie: {serial_number}\nDirección IP: {ip_address}"
        if messagebox.askyesno("Información del Sistema", f"{message}\n¿Desea guardar esta información en un archivo?"):
            save_system_info(system_name, serial_number, ip_address)

def show_menu():
    root = tk.Tk()
    root.title("Menú de Opciones")
    
    # Estilos
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    frame = tk.Frame(root, bg="#ffffff")
    frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text="Opciones del Sistema", font=("Arial", 16), bg="#ffffff")
    title_label.pack(pady=10)

    # Botones para cada opción
    delete_file_button = tk.Button(frame, text="Borrar Archivo", command=delete_file, bg="#ff4d4d", fg="#ffffff", font=("Arial", 12))
    delete_file_button.pack(pady=5, fill=tk.X)

    delete_folder_button = tk.Button(frame, text="Borrar Carpeta", command=delete_folder, bg="#ff4d4d", fg="#ffffff", font=("Arial", 12))
    delete_folder_button.pack(pady=5, fill=tk.X)

    get_mac_button = tk.Button(frame, text="Obtener Dirección MAC", command=get_mac_address, bg="#4d88ff", fg="#ffffff", font=("Arial", 12))
    get_mac_button.pack(pady=5, fill=tk.X)

    system_info_button = tk.Button(frame, text="Mostrar Información del Sistema", command=show_info_message, bg="#4d88ff", fg="#ffffff", font=("Arial", 12))
    system_info_button.pack(pady=5, fill=tk.X)

    exit_button = tk.Button(frame, text="Salir", command=root.quit, bg="#ffcc00", fg="#000000", font=("Arial", 14, "bold"))
    exit_button.pack(pady=5, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    run_as_admin()
    show_menu()
