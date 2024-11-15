import asyncio
import logging
import os
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

# Введите ваш API токен здесь
API_TOKEN = "8188228861:AAGyf_-m607R2rQRam6StU-WEymSfqylutg"
ADMIN_API_TOKEN = "8183576793:AAEmHSLcaypuyXkxoeUv5PY8HB2VIQFiL88"
ADMIN_CHAT_ID = "831450026"

# API URL администраторского бота
ADMIN_BOT_API_URL = "https://api.telegram.org/bot" + ADMIN_API_TOKEN + "/sendMessage"

# Переменная для хранения общего количества пользователей
total_users = 0
user_list = []


async def notify_admin(text):
    payload = {
        "chat_id": ADMIN_CHAT_ID,  # Замените на ID администратора или группового чата
        "text": text
    }
    try:
        requests.post(ADMIN_BOT_API_URL, data=payload)
    except Exception as e:
        logging.error(f"Ошибка отправки данных администратору: {e}")

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера с использованием хранилища в памяти
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определение кнопок меню
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Курс «Секреты женской силы»")],
        [KeyboardButton(text="Игра INTEGRA")],
        [KeyboardButton(text="Консультация")],
        [KeyboardButton(text="Оплата мероприятия")],
        [KeyboardButton(text="Контакты")]
    ],
    resize_keyboard=True
)

# Кнопки для записи на разные услуги
course_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Записаться «Секреты женской силы»")]],
    resize_keyboard=True
)

game_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Записаться «Игра INTEGRA»")]],
    resize_keyboard=True
)

consultation_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Записаться «Консультация»")]],
    resize_keyboard=True
)
pay_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Оплата мероприятий")]],
    resize_keyboard=True
)

# Словарь для хранения текущего контекста услуги для каждого пользователя
user_context = {}


# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    global total_users, user_list

    # Добавляем пользователя в список
    user_data = {"id": message.from_user.id, "name": message.from_user.username or message.from_user.first_name}
    user_list.append(user_data)
    total_users = len(user_list)

    # Уведомляем администратора
    users_info = "\n".join([f"UserID: {user['id']} - Имя: {user['name']}" for user in user_list])
    await notify_admin(f"Обновление списка пользователей:\n{users_info}\n\nОбщее число пользователей: {total_users}")
    user_context[message.from_user.id] = None
    await message.answer(
        f"Приветствую, {message.from_user.first_name}!\n Я — ваш виртуальный помощник и с радостью помогу найти тот самый курс, консультацию или мероприятие от Корн Татьяны, которые станут первыми шагами к важным внутренним открытиям и новым ощущениям. Хотите раскрыть свою женственность, научиться лучше понимать себя или вернуть гармонию в отношения? Здесь вы найдете именно то, что вам нужно:\n\n"
        "• *«КУРС «СЕКРЕТЫ ЖЕНСКОЙ СИЛЫ»* - если ты чувствуешь, что утратила связь с собой и нуждаешься в поддержке, то этот курс поможет наполниться энергией и раскрыть свою истинную силу через медитации, прямые эфиры и заботливую обратную связь. (25 €).\n\n"
        "• *«ИГРА INTEGRA»* - если хочешь изменить свою реальность и избавиться от внутренних блоков, (индивидуально 200 €, в группе 150 €), доступна в online и offline формате.\n\n"
        "• *«КОНСУЛЬТАЦИЯ»* - если тебе нужна поддержка и понимание, (50 € 1 час), доступна в online и offline формате.\n\n"
        "Давайте начнём ваш путь к внутренней гармонии и самовыражению! 💖\n"
        "Выбирайте, что откликается Вашему Сердцу ⬇️",
        parse_mode="Markdown",
        reply_markup=menu_keyboard
    )


# Обработчики кнопок
@dp.message(F.text == "Курс «Секреты женской силы»")
async def course_handler(message: Message):
    user_context[message.from_user.id] = "Курс"
    await message.answer(
        "У каждой женщины есть 5 ролей: королева, любовница, девочка, подруга, мать. Когда эти роли находятся в балансе, вы чувствуете гармонию и счастье. Но, к сожалению, очень часто происходит перекос и тогда всё идет не так, как нам бы хотелось…\n\n"
        "Этот канал служит проводником в вашу лучшую жизнь.\n\n"
        "Вас ждёт:\n"
        "🔹 3 медитации на принятие себя, любовь к себе и наполнение ресурсом.\n"
        "🔹 3 прямых эфира для активации и прокачки женских ролей. А также уберем ограничивающие убеждения, которые вам мешают расти.\n"
        "🔹 Моя поддержка на протяжении месяца.\n\n"
        "Когда? 18.11.2024г.\n"
        "Стоимость: 25€\n"
        "Формат: группа в Telegram\n\n",
    )
    await message.answer("🚀Для доступа жмите кнопку «Записаться»", reply_markup=course_keyboard)


@dp.message(lambda message: message.text == "Записаться «Секреты женской силы»")
async def course_registration_handler(message: Message):
    await message.answer(
        "Оплату 25 € можно совершить по следующим реквизитам:\n\n🇺🇦 Оплата в Украине\n"
        "👤 Получатель: Корн Тетяна Олександрівна\n🏦 Банк: Ukrsibbank\n💳 IBAN: UA943510050000026204808299625\n"
        "🏷️ Код ЕГРПОУ: 3161324545\n\n🇨🇭 Оплата в Швейцарии\n👤 Получатель: Tetiana Korn\n"
        "🏦 Банк: PostFinance\n💳 IBAN: CH61 0900 0000 1623 1622 9\n🔤 SWIFT/BIC: POFICHBEXXX\n"
        "🌍 Страна: Switzerland\n\n 🌐 Оплата через PayPal\n📧 Email: korntani.therapy@gmail.com\n\n"
        "Дублируем ниже счета для удобства.\nПришлите квитанцию или скриншот про оплату чтобы перейти к следующему шагу 🙌\n\n"
        "✉️ Если возникли вопросы пишите @korntani"
    )
    await message.answer("UA943510050000026204808299625")
    await message.answer("CH6109000000162316229")
    await message.answer("korntani.therapy@gmail.com")


@dp.message(lambda message: message.text == "Игра INTEGRA")
async def game_handler(message: Message):
    user_context[message.from_user.id] = "Игра"
    await message.answer(
        "✨ Трансформационная игра INTEGRA — это твой квантовый скачок в реальность, где желания достижимы.\n\n"
        "🔹 Для чего игра?\n"
        "Она поможет тебе выйти за рамки привычного восприятия, освободиться от блоков и ограничивающих убеждений, а также исцелить внутренние конфликты и травмы прошлого.\n\n"
        "🔹 Что ждет в процессе?\n"
        "Ты пройдешь трансформацию на всех уровнях — тело, эмоции, разум — под чутким сопровождением мастера.\n\n"
        "🔹 Что в итоге?\n"
        "Перестраивая свою внутреннюю «матрицу», ты создашь новую ветку реальности, где цели и мечты становятся реальными и достижимыми!"
        "Игра INTEGRA доступна в online и offline формате.\n\n",
    )
    await message.answer("Для записи на игру жмите «Записаться»", reply_markup=game_keyboard)


@dp.message(lambda message: message.text == "Записаться «Игра INTEGRA»")
async def course_registration_handler(message: Message):
    await message.answer(
        "Оплату 200€ (игра индивидуально) / 150€ (игра в группе) можно совершить по следующим реквизитам:\n\n🇺🇦 Оплата в Украине\n"
        "👤 Получатель: Корн Тетяна Олександрівна\n🏦 Банк: Ukrsibbank\n💳 IBAN: UA943510050000026204808299625\n"
        "🏷️ Код ЕГРПОУ: 3161324545\n\n🇨🇭 Оплата в Швейцарии\n👤 Получатель: Tetiana Korn\n"
        "🏦 Банк: PostFinance\n💳 IBAN: CH61 0900 0000 1623 1622 9\n🔤 SWIFT/BIC: POFICHBEXXX\n"
        "🌍 Страна: Switzerland\n\n 🌐 Оплата через PayPal\n📧 Email: korntani.therapy@gmail.com\n\n"
        "Дублируем ниже счета для удобства.\nПришлите квитанцию или скриншот про оплату чтобы перейти к следующему шагу 🙌\n\n"
        "✉️ Если возникли вопросы пишите @korntani"
    )
    await message.answer("UA943510050000026204808299625")
    await message.answer("CH6109000000162316229")
    await message.answer("korntani.therapy@gmail.com")


@dp.message(F.text == "Консультация")
async def consultation_handler(message: Message):
    user_context[message.from_user.id] = "Консультация"
    await message.answer(
        "🌸 Я помогу тебе комплексно и глубинно разобраться с запросом, чтобы ты смогла освободиться от негатива и заложить основу для счастливой, наполненной жизни.\n\n"
        "Использую уникальный микс методов — от гештальт-терапии и энергопрактик до МАК-карт и медитаций. \n\n"
        "📈 Это позволяет достичь результата максимально быстро и эффективно.\n"
        "Консультация доступна в online и offline формате.\n",
    )
    await message.answer("Готова к изменениям? Жми на кнопку «Записаться» и жду тебя на консультацию!",
                         reply_markup=consultation_keyboard)


@dp.message(F.text == "Записаться «Консультация»")
async def consultation_registration_handler(message: Message):
    await message.answer(
        "Оплату 50€ (за 1 час) можно совершить по следующим реквизитам:\n\n🇺🇦 Оплата в Украине\n"
        "👤 Получатель: Корн Тетяна Олександрівна\n🏦 Банк: Ukrsibbank\n💳 IBAN: UA943510050000026204808299625\n"
        "🏷️ Код ЕГРПОУ: 3161324545\n\n🇨🇭 Оплата в Швейцарии\n👤 Получатель: Tetiana Korn\n"
        "🏦 Банк: PostFinance\n💳 IBAN: CH61 0900 0000 1623 1622 9\n🔤 SWIFT/BIC: POFICHBEXXX\n"
        "🌍 Страна: Switzerland\n\n 🌐 Оплата через PayPal\n📧 Email: korntani.therapy@gmail.com\n\n"
        "Дублируем ниже счета для удобства.\nПришлите квитанцию или скриншот про оплату чтобы перейти к следующему шагу 🙌\n\n"
        "✉️ Если возникли вопросы пишите @korntani"
    )
    await message.answer("UA943510050000026204808299625")
    await message.answer("CH6109000000162316229")
    await message.answer("korntani.therapy@gmail.com")


# Обработчик для кнопки "Оплата мероприятия"
@dp.message(F.text == "Оплата мероприятия")
async def event_payment_handler(message: Message):
    user_context[message.from_user.id] = "Оплата"

    # Первое сообщение с реквизитами для оплаты
    await message.answer(
        "Оплату можно совершить по следующим реквизитам:\n\n"
        "🇺🇦 Оплата в Украине\n"
        "👤 Получатель: Корн Тетяна Олександрівна\n"
        "🏦 Банк: Ukrsibbank\n"
        "💳 IBAN: UA943510050000026204808299625\n"
        "🏷️ Код ЕГРПОУ: 3161324545\n\n"
        "🇨🇭 Оплата в Швейцарии\n"
        "👤 Получатель: Tetiana Korn\n"
        "🏦 Банк: PostFinance\n"
        "💳 IBAN: CH61 0900 0000 1623 1622 9\n"
        "🔤 SWIFT/BIC: POFICHBEXXX\n"
        "🌍 Страна: Switzerland\n\n"
        "🌐 Оплата через PayPal\n"
        "📧 Email: korntani.therapy@gmail.com\n\n"
        "Дублируем ниже счета для удобства.\n"
        "Пришлите квитанцию или скриншот про оплату, чтобы перейти к следующему шагу 🙌\n\n"
        "✉️ Если возникли вопросы пишите @korntani"
    )

    # Дополнительные сообщения с реквизитами для копирования
    await message.answer("UA943510050000026204808299625")
    await message.answer("CH61 0900 0000 1623 1622 9")
    await message.answer("korntani.therapy@gmail.com")

    # Запрос на отправку файла с подтверждением
    await message.answer(
        "Отправьте, пожалуйста, квитанцию или скриншот для подтверждения оплаты.",
        reply_markup=pay_keyboard
    )


@dp.message(lambda message: message.text == "Контакты", )
async def game_handler(message: Message):
    await message.answer(
        "📲 Мессенджеры: +380672400799\n\n 📞 Звонить: +41784228563")


# Обработчик для получения файлов и фото с категоризацией по услугам
@dp.message(F.document | F.photo)
async def handle_any_files(message: Message):
    service = user_context.get(message.from_user.id, "Другие")  # Получаем текущую категорию
    folder_path = os.path.join("downloads", service)
    os.makedirs(folder_path, exist_ok=True)

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_name = f"{file_id}.jpg"

    file_path = os.path.join(folder_path, file_name)

    try:
        # Получаем файл
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, file_path)

        # Благодарственное сообщение для каждой услуги
        if service == "Курс":
            await message.answer(
                "Благодарим за участие в курсе «Секреты женской силы»! 💖\n Ваш файл успешно получен.\n Присоединяйтесь к нашей группе, чтобы начать путешествие к женской гармонии ➡️ https://t.me/+nZ7Z13R5rm1mZGYy")
        elif service == "Игра":
            await message.answer(
                "Благодарю за доверие 💞\n Для уточнения даты, времени и формата проведения Игры «INTEGRA» напишите @korntani")
        elif service == "Консультация":
            await message.answer(
                "Благодарю за доверие 💞\n Для уточнения даты и времени проведения консультации напишите @korntani")
        elif service == "Оплата":
            await message.answer(
                "Благодарю за доверие 💞 Для уточнения информации напишите @korntan")
        else:
            await message.answer("Благодарим за доверие 💞 Ваш файл успешно получен!")

    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении файла: {e}")


# Асинхронная функция для запуска бота
async def main():
    await dp.start_polling(bot)


# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())