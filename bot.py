import os
import requests
from telegram import Bot

# Récupération des variables d'environnement
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def get_top_memecoins():
    url = "https://api.birdeye.so/public/markets" 
    headers = {"x-api-key": os.getenv("BIRDEYE_API_KEY")}  
    response = requests.get(url, headers=headers).json()

    response = requests.get(url, headers=headers)

print("Réponse brute:", response.text)

try:
    data = response.json()
    return data["data"]   
except ValueError:
    print("La réponse n'est pas au format JSON ou elle est vide.")
    return []
    
    top_tokens = [
        token for token in response["data"]
        if token["liquidity"] > 10
    ]

    return top_tokens

def send_alert():
    tokens = get_top_memecoins()
    if tokens:
        message = "🚀 **Memecoins Pumping** 🚀\n\n"
        for token in tokens[:5]: 
            message += f"🔹 {token['symbol']} | 💰 {token['liquidity']} SOL\n"
        
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    send_alert()
