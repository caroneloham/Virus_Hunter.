import os
import time
import json
import vt
from datetime import datetime


def lancer_analyse():
    global dossier_analyse
    API_KEY = '1e355f1556a70589da09036c4e093998e5bb9d21259199e0393bf39acc659b6b'
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Répertoire du script
    folder_path = os.path.join(script_dir, 'jeu_essaie')  # Chemin du dossier à analyser
    results = {}

    # Fonction pour analyser un fichier
    def scan_file(file_path):
        with open(file_path, 'rb') as f:
            client = vt.Client(API_KEY)
            analysis = client.scan_file(f, wait_for_completion=True)
            analysis = client.get_object("/analyses/{}", analysis.id)
            return analysis.results

    # Fonction pour analyser un répertoire
    def scan_directory(folder_path):
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                print(f"Scanning {file_path}")  # Affichage dans la console
                file_results = scan_file(file_path)
                results[file_path] = file_results
                time.sleep(2)

    # Fonction pour lire le fichier virus_hunter.cfg et analyser les répertoires mentionnés
    def lire_config_et_analyser():
        config_path = os.path.join(script_dir, 'jeu_essaie', 'virus_hunter.cfg')  # Chemin du fichier de configuration
        with open(config_path, 'r') as config_file:
            lines = config_file.readlines()[:3]  # Lire les 3 premières lignes
            for line in lines:
                folder_to_scan = line.strip()  # Retirer les espaces et les sauts de ligne
                print(f"Analyzing folder: {folder_to_scan}")  # Affichage dans la console
                scan_directory(folder_to_scan)

        # Écrire les résultats dans un fichier JSON
        log_results(results)

    # Fonction pour écrire les résultats dans un fichier journal
    def log_results(results):
        log_dir = os.path.join(script_dir, 'logs')  # Répertoire pour les fichiers journaux
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        now = datetime.now()
        log_file = os.path.join(log_dir, f"analysis_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json")
        with open(log_file, 'w') as f:
            json.dump(results, f, indent=4)

        # Lire et traiter le fichier log une fois qu'il a été créé
        traiter_fichier_log(log_file)

    # Fonction pour traiter le fichier log une fois qu'il a été créé
    def traiter_fichier_log(chemin_fichier_log):
        log_data = lire_fichier_log(chemin_fichier_log)
        for fichier, resultats in log_data.items():
            menace_identifiee = False
            for moteur, result_data in resultats.items():
                if result_data['result'] is not None:
                    menace_identifiee = True
                    # Passer le chemin du fichier log et la menace identifiée à la fonction enregistrer_menace_identifiee
                    enregistrer_menace_identifiee(chemin_fichier_log, fichier, result_data['result'])
                    break
            if not menace_identifiee:
                print(f"Aucune menace identifiée pour le fichier : {fichier}")

    # Fonction pour lire le fichier log
    def lire_fichier_log(chemin_fichier):
        with open(chemin_fichier, 'r') as f:
            log_data = json.load(f)
        return log_data

    # Fonction pour enregistrer les menaces identifiées dans le fichier log
    def enregistrer_menace_identifiee(log_file_path, nom_fichier, menace):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Enregistrement dans le fichier de journal
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"--- Menace identifiée ---\n")
            log_file.write(f"Date et heure : {current_datetime}\n")
            log_file.write(f"Fichier : {nom_fichier}\n")
            log_file.write(f"Menace identifiée : {menace}\n\n")

        # Enregistrement dans le fichier menace_identifiee.txt dans le dossier logs
        logs_dir = os.path.dirname(log_file_path)
        menace_file_path = os.path.join(logs_dir, 'menace_identifiee.log')
        with open(menace_file_path, 'a') as menace_file:
            menace_file.write(f"--- Menace identifiée ---\n")
            menace_file.write(f"Date et heure : {current_datetime}\n")
            menace_file.write(f"Fichier : {nom_fichier}\n")
            menace_file.write(f"Menace identifiée : {menace}\n\n")

    lire_config_et_analyser()


lancer_analyse()
