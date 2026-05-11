#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weather-news-bot v1.0
Telegram bot para alertas de clima y noticias.
Uso: python bot.py <TOKEN>
"""

import sys
import json
import urllib.request
import urllib.error
import re
from datetime import datetime

# --- CONFIGURACIÓN ---
CITY = "Madrid"  # Cambiar según ubicación
COUNTRY_CODE = "ES"  # Código de país para clima
RSS_NEWS = "http://feeds.bbci.co.uk/news/world/rss.xml"

# --- UTILIDADES ---
def fetch_url(url):
    """Descarga contenido de una URL con timeout y user-agent."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error al obtener datos: {e}"

# --- CLIMA (Open-Meteo) ---
def get_weather():
    """Obtiene clima actual usando coordenadas (Madrid por defecto)."""
    # Coordenadas de Madrid: 40.4168, -3.7038
    lat, lon = 40.4168, -3.7038
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = fetch_url(url)
    try:
        json_data = json.loads(data)
        if "current_weather" in json_data:
            cw = json_data["current_weather"]
            return (f"🌤️ *Clima en {CITY} ({datetime.now().strftime('%H:%M')})*\n"
                    f"Temperatura: {cw['temperature']}°C\n"
                    f"Viento: {cw['windspeed']} km/h\n"
                    f"Dirección: {cw.get('winddirection', 'N/A')}°")
        else:
            return "❌ No se pudo obtener el clima. Intente más tarde."
    except json.JSONDecodeError:
        return f"❌ Error al procesar datos del clima.\n{data[:200]}..."

# --- NOTICIAS (RSS simple con regex) ---
def get_news(limit=3):
    """Obtiene las primeras `limit` noticias del RSS de BBC World."""
    xml = fetch_url(RSS_NEWS)
    # Regex para extraer <title> y <link> (simplificado para RSS estándar)
    titles = re.findall(r'<title>([^<]+)</title>', xml)
    links = re.findall(r'<link>([^<]+)</link>', xml)
    if len(titles) < 2 or len(links) < 2:
        return "❌ No se pudieron cargar las noticias."
    # Ignorar primeros 2 títulos (RSS feed title + channel title)
    result = ["📰 *Últimas Noticias (BBC World)*\n"]
    for i in range(2, min(2 + limit, len(titles))):
        title = titles[i].replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        link = links[i] if i < len(links) else "#"
        result.append(f"• [{title}]({link})")
    return "\n".join(result)

# --- EJECUTABLE (CLI para pruebas) ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python bot.py <TELEGRAM_BOT_TOKEN>")
        print("\nPruebas locales:")
        print("\n--- CLIMA ---")
        print(get_weather())
        print("\n--- NOTICIAS ---")
        print(get_news())
    else:
        token = sys.argv[1]
        print(f"✅ Bot iniciado con token: {token[:8]}... (simulación)")
        print("Ejecute comandos: /weather, /news")
        # Aquí iría la lógica real con python-telegram-bot
        print("\nNota: Para producción, instalar: pip install python-telegram-bot")
