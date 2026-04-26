import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤️ Привіт! Я бот погоди!\n\n"
        "Напиши команду:\n"
        "/weather Kyiv\n"
        "/weather London\n"
        "/weather New York"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Напиши місто! Наприклад: /weather Kyiv")
        return
    
    city = " ".join(context.args)
    
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        current = data['current_condition'][0]
        temp = current['temp_C']
        feels = current['FeelsLikeC']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        visibility = current['visibility']
        pressure = current['pressure']
        
        msg = (
            f"🌍 *Погода в {city}*\n\n"
            f"🌡️ Температура: *{temp}°C*\n"
            f"🤔 Відчувається як: *{feels}°C*\n"
            f"☁️ Опис: *{desc}*\n\n"
            f"💧 Вологість: *{humidity}%*\n"
            f"💨 Вітер: *{wind} км/год*\n"
            f"👁️ Видимість: *{visibility} км*\n"
            f"🔵 Тиск: *{pressure} гПа*"
        )
        
        await update.message.reply_text(msg, parse_mode='Markdown')
        
    except:
        await update.message.reply_text("❌ Місто не знайдено! Спробуй англійською.")

app = Application.builder().token("ТВІЙ_ТОКЕН").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("weather", weather))

print("Бот погоди запущено! 🌤️")
app.run_polling()
