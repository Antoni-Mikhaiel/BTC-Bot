import requests
import pandas as pd
import time
from ta.momentum import RSIIndicator

from config import BOT_TOKEN, CHAT_ID, SYMBOL, INTERVAL, RSI_PERIOD

def get_data():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=100"
    data = requests.get(url).json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","trades","tbbav","tbqav","ignore"
    ])

    df["close"] = df["close"].astype(float)
    return df

def calculate_rsi(df):
    rsi = RSIIndicator(close=df["close"], window=RSI_PERIOD)
    return rsi.rsi().iloc[-1]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def main():
    alerted = False

    while True:
        try:
            df = get_data()
            rsi = calculate_rsi(df)

            print(f"RSI: {rsi:.2f}")

            if rsi < 30 and not alerted:
                send_telegram(f"🚨 BTC RSI BELOW 30: {rsi:.2f}")
                alerted = True

            if rsi > 35:
                alerted = False

        except Exception as e:
            print("Error:", e)

        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print("Shutting down cleanly")
            break

        except KeyboardInterrupt:
            print("Bot stopped gracefully (SIGINT received)")

if __name__ == "__main__":
    main()