import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from weather import get_weather, get_temp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    if jobs:
        await update.message.reply_text("Ты уже подписан на погоду.")
        return

    await update.message.reply_text(
        "Привет! Это мой первый бот. Верити не верити"
    )

    moscow = ZoneInfo("Europe/Moscow")

    next_hour = (
    datetime.now(moscow)
    .replace(minute=0, second=0, microsecond=0)
    + timedelta(hours=1)
)

    context.job_queue.run_repeating(   

        send_weather,
        interval=3600,
        first=next_hour,
        chat_id=chat_id,
        name=str(chat_id)
)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    if not jobs:
        await update.message.reply_text("Ты не подписан на рассылку.")
        return

    for job in jobs:
        job.schedule_removal()

    await update.message.reply_text("Почасовая рассылка отключена.")

async def send_weather(context):
    weather_data = get_weather()

    temperature, precipitation, current_time = get_temp(weather_data)

    message = (
        f"Погода на {current_time}\n"
        f"Температура: {temperature} °C\n"
        f"Осадки: {precipitation} мм"
    )

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=message
    )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    app.run_polling()


if __name__ == "__main__":
    main()