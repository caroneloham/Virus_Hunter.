import vonage
from datetime import datetime

# Remplacez 'VOTRE_API_KEY' et 'VOTRE_API_SECRET' par vos propres clés API Vonage
client = vonage.Client(key='7KtRfN2uT8m6a1PQ9fj3PQ7kR5sN2uT8m6a1PQ9fj3PQ7kR5sN2uT8m6a1', secret='pK6qZ8vE2rS4tY0mB3nI5cJ7oL9')
sms = vonage.Sms(client)

# Corps du message
message = """
Bonjour,

Nous vous informons que l'analyse "virus_hunter" est désormais complète. Tous les détails relatifs aux résultats ainsi que les éventuelles recommandations ont été transmis à votre adresse e-mail associée.

Si vous avez des questions ou besoin d'assistance supplémentaire, n'hésitez pas à nous contacter.

Nous vous remercions pour votre confiance.

Cordialement,
L'équipe VirusHunter
{}

""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Remplacez 'NUMERO_DESTINATAIRE' par le numéro de téléphone du destinataire
response = sms.send_message({
    'from': 'VonageAPI',
    'to': '0630392183',
    'text': message
})

if response['messages'][0]['status'] == '0':
    print("SMS envoyé avec succès.")
else:
    print(f"Échec de l'envoi du SMS. Statut: {response['messages'][0]['status']}")
