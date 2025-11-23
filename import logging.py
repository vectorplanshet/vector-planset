import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import folium
import os

# Токен от BotFather
TELEGRAM_API_TOKEN = '8134774526:AAEDL9zE7X326VX3K-8LyIA63lfQpAveqfQ'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для отправки карты
def create_map(latitude: float, longitude: float) -> str:
    # Создание карты с маркером
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker([latitude, longitude]).add_to(m)
    
    # Сохраняем карту как HTML
    map_path = 'index.html'
    m.save(map_path)
    return map_path

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Отправь мне координаты в формате 'широта, долгота'.")

# Обработчик текста с координатами
def handle_coordinates(update: Update, context: CallbackContext) -> None:
    try:
        coords = update.message.text.split(',')
        lat = float(coords[0].strip())
        lon = float(coords[1].strip())

        # Создание карты
        map_path = create_map(lat, lon)

        # Отправка карты пользователю
        with open(map_path, 'rb') as map_file:
            update.message.reply_photo(photo=map_file)

        # Удаляем временный файл карты
        os.remove(map_path)
    except ValueError:
        update.message.reply_text("Некорректный формат. Отправь координаты в формате 'широта, долгота'.")

# Основная функция
def main() -> None:
    # Создание объекта Updater
    updater = Updater(TELEGRAM_API_TOKEN)

    # Получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_coordinates))

    # Запуск бота
    updater.start_polling()

    # Ожидаем завершения
    updater.idle()

if __name__ == '__main__':
    main()
