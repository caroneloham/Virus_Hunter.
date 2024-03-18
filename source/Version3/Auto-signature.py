import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.ttk import Style
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from datetime import datetime, timedelta

def generate_certificate(domain, country, state, locality, organization, password):
    try:
        # Validation du code pays à deux lettres
        if len(country) != 2:
            raise ValueError("Le code pays doit être de deux lettres.")

        # Générer une clé privée RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Créer un certificat auto-signé
        subject = issuer = x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, domain),
        ])

        certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(domain)]),
            critical=False
        ).sign(private_key, hashes.SHA256(), default_backend())

        # Exporter la clé privée et le certificat en format PFX
        pfx = pkcs12.serialize_key_and_certificates(
            name=b'my_certificate',
            key=private_key,
            cert=certificate,
            cas=None,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
        )

        with open(f"{domain}.pfx", "wb") as pfx_file:
            pfx_file.write(pfx)

        messagebox.showinfo("Succès", f"Le certificat PFX pour {domain} a été créé avec succès.")
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

def create_gui():
    app = tk.Tk()
    app.geometry("400x300")
    app.title("Générateur de certificat")

    # Thème bleu
    style = Style()
    style.theme_use('clam')

    # Icône
    app.iconbitmap('icone.ico')

    domain_var = tk.StringVar()
    country_var = tk.StringVar()
    state_var = tk.StringVar()
    locality_var = tk.StringVar()
    organization_var = tk.StringVar()

    tk.Label(app, text="Nom de Domaine:").pack()
    tk.Entry(app, textvariable=domain_var).pack()

    tk.Label(app, text="Pays (Ex: FR):").pack()
    tk.Entry(app, textvariable=country_var).pack()

    tk.Label(app, text="État/Province:").pack()
    tk.Entry(app, textvariable=state_var).pack()

    tk.Label(app, text="Localité:").pack()
    tk.Entry(app, textvariable=locality_var).pack()

    tk.Label(app, text="Organisation:").pack()
    tk.Entry(app, textvariable=organization_var).pack()

    def submit():
        domain = domain_var.get()
        country = country_var.get()
        state = state_var.get()
        locality = locality_var.get()
        organization = organization_var.get()
        password = simpledialog.askstring("Password", "Entrez le mot de passe pour le fichier PFX:", show='*')
        if password:
            generate_certificate(domain, country, state, locality, organization, password)
        else:
            messagebox.showwarning("Annulé", "La création du certificat a été annulée.")

    tk.Button(app, text="Créer Certificat", command=submit).pack()

    app.mainloop()

if __name__ == "__main__":
    create_gui()
