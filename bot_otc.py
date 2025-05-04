import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from telegram import Bot
import time

# === DATOS DE TELEGRAM ===
TOKEN = '8143892218:AAHQYwbFq4N1L3LwzO66vLrhDVM9TkznEPg'
CHAT_ID = '8020694910'

bot = Bot(token=TOKEN)

# Para evitar repetir señales
ultima_senal = None

# === FUNCION DE DATOS (SIMULADOS POR AHORA) ===
def obtener_datos():
    # Crea un DataFrame con velas simuladas (puedes conectar API o archivo CSV real)
    data = {
        'close': [1.151, 1.152, 1.153, 1.150, 1.148, 1.145, 1.140, 1.135, 1.130, 1.128, 1.125, 1.122, 1.120, 1.117, 1.115],
    }
    df = pd.DataFrame(data)
    return df

# === APLICA INDICADORES ===
def aplicar_indicadores(df):
    df['EMA'] = EMAIndicator(close=df['close'], window=14).ema_indicator()
    df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()
    return df

# === DETECTA Y GENERA LA SEÑAL ===
def detectar_senal(df):
    global ultima_senal
    ultima_fila = df.iloc[-1]
    rsi = ultima_fila['RSI']

    if rsi < 30 and ultima_senal != 'CALL':
        ultima_senal = 'CALL'
        return "📈 Señal OTC: CALL\n(RSI < 30)"
    elif rsi > 70 and ultima_senal != 'PUT':
        ultima_senal = 'PUT'
        return "📉 Señal OTC: PUT\n(RSI > 70)"
    return None

# === ENVÍA A TELEGRAM ===
def enviar_telegram(mensaje):
    bot.send_message(chat_id=CHAT_ID, text=mensaje)

# === CICLO PRINCIPAL ===
def iniciar_bot():
    print("🔄 Bot iniciado. Esperando condiciones para enviar señales...")
    while True:
        try:
            df = obtener_datos()
            df = aplicar_indicadores(df)
            senal = detectar_senal(df)
            if senal:
                print("✅ Señal detectada, enviando a Telegram...")
                enviar_telegram(senal)
            time.sleep(60)  # espera 1 minuto antes de volver a analizar
        except Exception as e:
            print("❌ Error:", e)
            time.sleep(60)

# === EJECUTA EL BOT ===
if __name__ == "__main__":
    iniciar_bot()
