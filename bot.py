import os
import requests

# Fonction pour récupérer les tokens avec une grande liquidité
def get_top_memecoins():
    try:
        url = os.getenv("API_URL")  # L'URL de l'API sera stockée dans la variable d'environnement API_URL
        api_key = os.getenv("API_KEY")  # La clé API sera stockée dans la variable d'environnement API_KEY
        headers = {"x-api-key": api_key}
        response = requests.get(url, headers=headers)

        print("Réponse brute:", response.text)  # Affiche la réponse complète avant la conversion en JSON

        # Vérifie si la réponse est au format JSON avant de l'utiliser
        if response.status_code == 200:
            try:
                data = response.json()  # Essaie de convertir la réponse en JSON
                return data["data"]      # Retourne les données si la conversion réussie
            except ValueError:
                print("La réponse n'est pas au format JSON ou elle est vide.")
                return []  # Retourne une liste vide si la réponse n'est pas JSON
        else:
            print(f"Erreur API: {response.status_code} - {response.text}")
            return []  # Retourne une liste vide si l'API retourne une erreur
    except requests.exceptions.RequestException as e:
        print(f"Erreur pendant l'appel API : {e}")
        return []  # Retourne une liste vide en cas d'erreur réseau

# Fonction pour envoyer un message sur Telegram avec les tokens récupérés
def send_alert():
    tokens = get_top_memecoins()
    if tokens:
        message = f"Top Memecoins avec une grande liquidité :\n"
        for token in tokens:
            message += f"Token: {token['name']}, Symbole: {token['symbol']}, Liquidité: {token['liquidity']}\n"
        send_telegram_message(message)
    else:
        send_telegram_message("Aucun token trouvé ou une erreur est survenue.")

# Fonction pour envoyer un message sur Telegram
def send_telegram_message(message):
    token = os.getenv("TELEGRAM_TOKEN")  # Le token du bot Telegram est stocké dans la variable d'environnement TELEGRAM_TOKEN
    chat_id = os.getenv("TELEGRAM_CHAT_ID")  # L'ID du chat est stocké dans la variable d'environnement TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Message envoyé avec succès.")
    else:
        print(f"Erreur en envoyant le message : {response.text}")

# Appeler la fonction d'envoi d'alertes
send_alert()
