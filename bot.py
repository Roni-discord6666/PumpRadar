import os
import requests
from telegram import Bot

# Récupération des variables d'environnement
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# Fonction pour récupérer les memecoins Pump.fun avec grosse liquidité
def get_top_memecoins():
    url = "https://api.birdeye.so/public/markets"  # API pour récupérer les tokens
    headers = {"x-api-key": os.getenv("BIRDEYE_API_KEY")}  # Clé API à ajouter
    response = requests.get(url, headers=headers).json()

    response = requests.get(url, headers=headers)

print("Réponse brute:", response.text)  # Affiche la réponse complète, avant la conversion en JSON

try:
    data = response.json()  # Essaie de décoder en JSON
    return data["data"]      # Si le JSON est valide, utilise-le
except ValueError:
    print("La réponse n'est pas au format JSON ou elle est vide.")
    return []

    # Filtrer les tokens avec grosse liquidité
    top_tokens = [
        token for token in response["data"]
        if token["liquidity"] > 10  # Exemple : 10 SOL minimum
    ]

    return top_tokens

# Fonction pour envoyer l'alerte Telegram
def send_alert():
    tokens = get_top_memecoins()
    if tokens:
        message = "🚀 **Memecoins Pumping** 🚀\n\n"
        for token in tokens[:5]:  # Limite aux 5 meilleurs
            message += f"🔹 {token['symbol']} | 💰 {token['liquidity']} SOL\n"
        
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

# Exécuter l'alerte quand le script tourne
if __name__ == "__main__":
    send_alert()
