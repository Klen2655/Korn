import asyncio
import logging
import os
import csv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Вставьте API токен администратора
ADMIN_API_TOKEN = "8183576793:AAEmHSLcaypuyXkxoeUv5PY8HB2VIQFiL88"
ADMIN_CHAT_ID = "831450026"  # ID администратора

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
admin_bot = Bot(token=ADMIN_API_TOKEN)
admin_dp = Dispatcher()

# Путь к файлу для хранения информации о пользователях
USER_DATA_FILE = "user_data.csv"


# Функция для записи данных пользователя в файл
def save_user_data(user_id, username, first_name):
    file_exists = os.path.exists(USER_DATA_FILE)

    with open(USER_DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["User ID", "Username", "First Name"])  # Заголовки
        writer.writerow([user_id, username, first_name])


# Функция для получения списка пользователей
def get_users():
    if not os.path.exists(USER_DATA_FILE):
        return "Нет пользователей."

    with open(USER_DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        users = list(reader)[1:]  # Пропускаем заголовки
        if not users:
            return "Список пользователей пуст."

        user_list = "\n".join([f"UserID: {user[0]} - Имя: {user[1]} {user[2]}" for user in users])
        return f"Список пользователей:\n{user_list}"


# Функция для получения статистики
def get_stats():
    if not os.path.exists(USER_DATA_FILE):
        return "Нет данных для статистики."

    with open(USER_DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        users = list(reader)[1:]  # Пропускаем заголовки
        total_users = len(users)
        return f"Статистика:\nОбщее число пользователей: {total_users}"


# Обработчик команды /start для администратора
@admin_dp.message(Command("start"))
async def start_admin(message: types.Message):
    # Просто приветственное сообщение без кнопок
    await message.answer("Добро пожаловать в админ-бот KornTani_admin.\n")


# Обработчик команды /users для отображения списка пользователей
@admin_dp.message(Command("users"))
async def show_users(message: types.Message):
    users_list = get_users()
    await message.answer(users_list)


# Обработчик команды /stats для отображения статистики
@admin_dp.message(Command("stats"))
async def show_stats(message: types.Message):
    stats_info = get_stats()
    await message.answer(stats_info)


# Обработчик команды /start для добавления пользователя в список
@admin_dp.message(Command("start"))
async def start_client(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    first_name = message.from_user.first_name

    # Сохраняем данные пользователя в файл
    save_user_data(user_id, username, first_name)

    # Отправляем приветственное сообщение пользователю
    await message.answer(
        f"Привет, {first_name}!\nДобро пожаловать в наш сервис! Вы были добавлены в список пользователей."
    )


# Запуск администратора
async def main():
    await admin_dp.start_polling(admin_bot)


if __name__ == "__main__":
    asyncio.run(main())
