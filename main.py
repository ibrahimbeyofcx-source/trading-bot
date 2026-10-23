import time
import ccxt
import requests

TELEGRAM_TOKEN = "8749846693:AAG64N-Y9kBHMaKWABbGHXDG7SbEeuLt3g"
CHAT_ID = "5402908350"
COINLER = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
exchange = ccxt.binance()


def mesaj_gonder(mesaj):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": mesaj}
  try:
    requests.post(url, json=payload)
  except Exception as e:
    print(f"Mesaj gönderme hatası: {e}")


def rsi_hesapla(fiyatlar, periyot=14):
  if len(fiyatlar) < periyot + 1:
    return 50
  farklar = [fiyatlar[i] - fiyatlar[i - 1] for i in range(1, len(fiyatlar))]
  kazanclar = [f if f > 0 else 0 for f in farklar]
  kayiplar = [-f if f < 0 else 0 for f in farklar]
  ort_kazanc = sum(kazanclar[-periyot:]) / periyot
  ort_kayip = sum(kayiplar[-periyot:]) / periyot
  if ort_kayip == 0:
    return 100
  rs = ort_kazanc / ort_kayip
  return 100 - (100 / (1 + rs))


mesaj_gonder("🚀 Trading Botu Render üzerinde başarıyla başlatıldı!")

while True:
  try:
    for sembol in COINLER:
      ohlcv = exchange.fetch_ohlcv(sembol, timeframe="15m", limit=30)
      kapanis_fiyatlari = [mum[4] for mum in ohlcv]
      son_fiyat = kapanis_fiyatlari[-1]
      rsi = rsi_hesapla(kapanis_fiyatlari)
      if rsi < 30:
        mesaj_gonder(
            f"🚨 ALIM SİNYALİ!\nCoin: {sembol}\nFiyat: ${son_fiyat}\nRSI:"
            f" {rsi:.2f}"
        )
      elif rsi > 70:
        mesaj_gonder(
            f"⚠️ SATIŞ SİNYALİ!\nCoin: {sembol}\nFiyat: ${son_fiyat}\nRSI:"
            f" {rsi:.2f}"
        )
    time.sleep(300)
  except Exception as e:
    print(f"Hata: {e}")
    time.sleep(60)
