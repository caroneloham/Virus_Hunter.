import subprocess
import sys

def show_certificate(file_path):
    try:
        # Exécution de la commande pour obtenir les informations du certificat
        result = subprocess.run(['certutil', '-v', '-dump', file_path], capture_output=True, text=True, check=True)
        certificate_info = result.stdout
        print(certificate_info)  # Affichage des informations du certificat dans la console
    except subprocess.CalledProcessError:
        print("Error: Certificate information not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <path_to_exe_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    show_certificate(file_path)
