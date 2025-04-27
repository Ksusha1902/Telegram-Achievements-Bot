import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

winners = {}
bot = Bot(token='YOUR BOT ID')
dp = Dispatcher()
my_id=YOUR ID
for_definite = []
lst_file_id_for1 = ['AgACAgIAAxkBAAIDg2fY-tdCl3MZkCXR0IL-yPkqo1AKAAKY7TEbqIHJSgRww7R6dpLGAQADAgADeAADNgQ','AgACAgIAAxkBAAIL7mfoELsQXJY_R7OeNl-WhFoB_To7AAIv8DEbo5RAS3reHOxbXuepAQADAgADeAADNgQ']
lst_file_id_for2 = ['AgACAgIAAxkBAAIVIWf03IDJPu5Ne1YZHG1_7TbvwsjjAAJc7TEblm6pS2kHKjBHwiN8AQADAgADeQADNgQ' ]
lst_file_id_for3 = ['AgACAgIAAxkBAAIVI2f03QRhwkTokU3enNur0WkN_RNrAAJg7TEblm6pS7bWyZUPBPaRAQADAgADeQADNgQ' ]
lst_file_id_for_participants = ['AgACAgIAAxkBAAIVJWf03Sq3KyANNkV61raRDJtBL1nHAAJj7TEblm6pS8JLhpl6f-2PAQADAgADeAADNgQ']

# Флаги для отслеживания ожидания ввода
waiting_for_event_name_for_definite = {}
waiting_for_winner_id_for_word = False
waiting_for_winner_id_for_word2 = False
waiting_for_winner_id_for_word3= False
waiting_for_winner_id_for_word4 = False

winners1_for_word = []
winners2_for_word = []
winners3_for_word = []
participant = []
participants_for_word=[]


def create_connection():
    conn = sqlite3.connect('events.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS Events')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            event_time TEXT NOT NULL,
            location TEXT NOT NULL,
            registration_deadline TEXT NOT NULL,
            max_participants INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,  
            contact_info TEXT NOT NULL  
        )
    ''')
    conn.commit()
    conn.close()


def add_event_to_db(event, user_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Проверка на уникальность
    cursor.execute('''
        SELECT * FROM Events WHERE event_name = ? AND event_date = ? AND event_time = ? AND location = ? AND user_id = ?
    ''', (event['name'], event['date'], event['time'], event['location'], user_id))

    if cursor.fetchone() is not None:
        print("Мероприятие уже существует в базе данных.")
        conn.close()
        return  # Выход из функции, если мероприятие уже существует

    cursor.execute('''
        INSERT INTO Events (event_name, event_date, event_time, location, registration_deadline, max_participants, user_id, event_type, contact_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
    ''', (event['name'], event['date'], event['time'], event['location'], event['registration_deadline'],
          event['max_participants'], user_id, event['type'], event['contact_info']))

    conn.commit()
    conn.close()


create_table()

def get_all_events(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Events WHERE user_id = ?', (user_id,))
    events = cursor.fetchall()  # Получаем все записи из таблицы для данного user_id
    conn.close()
    return events

def delete_last_event(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Получаем ID последнего мероприятия для данного пользователя
    cursor.execute('SELECT event_id FROM Events WHERE user_id = ? ORDER BY event_id DESC LIMIT 1', (user_id,))
    last_event = cursor.fetchone()

    if last_event is None:
        print("Нет мероприятий для удаления.")
        conn.close()
        return

    last_event_id = last_event[0]

    # Удаляем мероприятие по его ID
    cursor.execute('DELETE FROM Events WHERE event_id = ?', (last_event_id,))
    conn.commit()
    conn.close()

    print(f"Мероприятие с ID {last_event_id} успешно удалено.")


#вторая бд
def create_connection_winners():
    conn = sqlite3.connect('winners.db')
    return conn

def create_table_winners():
    conn = create_connection_winners()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS winners')  # Удаляем таблицу, если она существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS winners (
            winner_id INTEGER,
            место INTEGER,
            название TEXT,
            айдишка_картинки TEXT,
            user_id INTEGER,  -- Добавляем столбец user_id
            PRIMARY KEY (winner_id, название) 
        )
    ''')
    conn.commit()
    conn.close()



def get_all_winners(winner_id):
    conn = create_connection_winners()
    cursor = conn.cursor()
    cursor.execute('SELECT winner_id, место, название, айдишка_картинки FROM winners WHERE winner_id = ?', (winner_id,))
    winners = cursor.fetchall()
    conn.close()
    return winners


def add_winner_to_db(winner_data):
    conn = create_connection_winners()
    cursor = conn.cursor()
    try:
        query = """
                INSERT INTO winners (winner_id, место, название, айдишка_картинки, user_id)  -- Добавляем user_id
                VALUES (?, ?, ?, ?, ?)
                """
        cursor.execute(query, (winner_data['winner_id'], winner_data['место'], winner_data['название'], winner_data['айдишка_картинки'], winner_data['user_id']))  # Добавляем user_id
        conn.commit()
        print("Данные о победителе успешно сохранены:", winner_data)
    except Exception as e:
        print("Ошибка при сохранении данных в базу:", e)
    finally:
        conn.close()
create_table_winners()
#третья бд основа
def create_connection_events_for_world():
    conn = sqlite3.connect('events.db')
    return conn

def create_table_events_for_world():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS Events')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            event_time TEXT NOT NULL,
            location TEXT NOT NULL,
            registration_deadline TEXT NOT NULL,
            max_participants INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,  
            contact_info TEXT NOT NULL  
        )
    ''')
    conn.commit()
    conn.close()

def add_event_to_db_events_for_world(event, user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Events (event_name, event_date, event_time, location, registration_deadline, max_participants, user_id, event_type, contact_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
    ''', (event['name'], event['date'], event['time'], event['location'], event['registration_deadline'],
          event['max_participants'], user_id, event['type'], event['contact_info']))  # Добавлено значение contact_info
    conn.commit()
    conn.close()

create_table_events_for_world()


def get_all_events_events_for_world():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()  # Получаем все мероприятия
    conn.close()
    return events  # Возвращаем список всех мероприятий


def get_event_by_id(event_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events WHERE event_id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    return event

def add_second_place_to_db(second_place_data):
    conn = create_connection_winners()
    cursor = conn.cursor()
    try:
        query = """
                INSERT INTO winners (winner_id, место, название, айдишка_картинки, user_id)
                VALUES (?, ?, ?, ?, ?)
                """
        cursor.execute(query, (second_place_data['winner_id'], second_place_data['место'], second_place_data['название'], second_place_data['айдишка_картинки'], second_place_data['user_id']))
        conn.commit()
        print("Данные о втором месте успешно сохранены:", second_place_data)
    except Exception as e:
        print("Ошибка при сохранении данных о втором месте в базу:", e)
    finally:
        conn.close()
def add_third_place_to_db(third_place_data):
    conn = create_connection_winners()
    cursor = conn.cursor()
    try:
        query = """
                INSERT INTO winners (winner_id, место, название, айдишка_картинки, user_id)
                VALUES (?, ?, ?, ?, ?)
                """
        cursor.execute(query, (third_place_data['winner_id'], third_place_data['место'], third_place_data['название'], third_place_data['айдишка_картинки'], third_place_data['user_id']))
        conn.commit()
        print("Данные о третьем месте успешно сохранены:", third_place_data)
    except Exception as e:
        print("Ошибка при сохранении данных о третьем месте в базу:", e)
    finally:
        conn.close()
def add_participant_to_db(participant_data):
    conn = create_connection_winners()
    cursor = conn.cursor()
    try:
        query = """
                INSERT INTO winners (winner_id, место, название, айдишка_картинки, user_id)
                VALUES (?, ?, ?, ?, ?)
                """
        cursor.execute(query, (participant_data['winner_id'], participant_data['место'], participant_data['название'], participant_data['айдишка_картинки'], participant_data['user_id']))
        conn.commit()
        print("Данные об участнике успешно сохранены")
    except Exception as e:
        print("Ошибка при сохранении данных о участниках в базу:", e)
        # Выводим дополнительные данные для отладки
        print("Данные участника:", participant_data)
    finally:
        conn.close()


async def on_startup():
    print('Bot launched successfully.')


@dp.message(Command('start'))
async def cmd(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='Мои достижения'), types.KeyboardButton(text='Новые мероприятия')],
            [types.KeyboardButton(text='Мои мероприятия'), types.KeyboardButton(text='Создать мероприятие')]
        ],
        resize_keyboard=True
    )
    await message.answer('Добро пожаловать!Если у вас будут вопросы по боту то нажмите на /help \nПеред тем как использовать бота, советуем узнать свой ID и ID участников Вашего мероприятия. Это можно сделать, используя бота @useridinbotbot\n\nВыберите действие:', reply_markup=kb)

@dp.message(F.text == "Новые мероприятия")
async def new_events(message: types.Message):
    events = get_all_events_events_for_world()  # Получаем все мероприятия из базы данных
    print(events)

    if not isinstance(events, list) or not events:
        await message.answer("Нет новых мероприятий для общего пользования.")
        return

    public_events = []

    # Фильтруем мероприятия для общего пользования
    for event in events:
        if event[8] == 'Для общего пользования':  # Предполагаем, что тип мероприятия находится в 8-й колонке
            public_events.append(event)

    if public_events:
        response = "Мероприятия, в которых можно поучаствовать:\n"
        inline_kb = []
        for event in public_events:
            response += f"- {event[1]}\n"  # Добавляем название мероприятия в текст
            inline_kb.append([types.InlineKeyboardButton(text=event[1],
                                                         callback_data=f"q_{event[0]}")])  # Добавляем кнопку с названием мероприятия

        # Создаем инлайн-клавиатуру из списка кнопок
        inline_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)
        await message.answer(response, reply_markup=inline_kb_markup)
    else:
        await message.answer("Нет новых мероприятий для общего пользования.")

@dp.callback_query(lambda c: c.data.startswith('q_'))
async def show_event_details(callback_query: types.CallbackQuery):
    event_id = int(callback_query.data.split("_")[1])  # Получаем event_id из колбэка
    event = get_event_by_id(event_id)  # Получаем информацию о мероприятии по id
    print(event)
    if event:
        response = (
            f"Название: {event[1]}\n"
            f"Дата: {event[2]}\n"
            f"Время: {event[3]}\n"
            f"Место: {event[4]}\n"
            f"Крайний срок регистрации: {event[5]}\n"
            f"Максимальное количество участников: {event[6]}\n"
            f"Тип мероприятия: {event[8]}\n"
            f"Контактная информация: {event[9]}"
        )
        await callback_query.answer()  # Убираем уведомление о колбэке
        await callback_query.message.answer(response)  # Отправляем информацию о мероприятии
    else:
        await callback_query.answer("Мероприятие не найдено.")


@dp.message(F.text == "Создать мероприятие")
async def create_event(message: types.Message):

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Для общего пользования'),
                types.KeyboardButton(text='Для определенного круга людей')
            ],

        ],
        resize_keyboard=True
    )

    waiting_for_event_name_for_definite[message.from_user.id] = 'event_type'
    await message.answer("Выберите тип мероприятия:", reply_markup=kb)


@dp.message(lambda message: message.from_user.id in waiting_for_event_name_for_definite)
async def add_event(message: types.Message):
    user_id = message.from_user.id
    current_state = waiting_for_event_name_for_definite[user_id]

    if current_state == 'event_type':
        event_type = message.text
        if event_type not in ['Для общего пользования', 'Для определенного круга людей']:
            await message.answer("Пожалуйста, выберите корректный тип мероприятия.")
            return

        # Сохраняем тип мероприятия
        for_definite.append({"type": event_type, "user_id": user_id})
        waiting_for_event_name_for_definite[user_id] = 'event_name'
        await message.answer("Введите название мероприятия:")

    elif current_state == 'event_name':
        event_name = message.text
        for_definite[-1]['name'] = event_name
        waiting_for_event_name_for_definite[user_id] = 'event_date'
        await message.answer("Введите дату мероприятия (в формате ГГГГ-ММ-ДД):")

    elif current_state == 'event_date':
        event_date = message.text
        for_definite[-1]['date'] = event_date
        waiting_for_event_name_for_definite[user_id] = 'event_time'
        await message.answer("Введите время мероприятия (в формате ЧЧ:ММ):")

    elif current_state == 'event_time':
        event_time = message.text
        for_definite[-1]['time'] = event_time
        waiting_for_event_name_for_definite[user_id] = 'event_location'
        await message.answer("Введите место проведения мероприятия:")

    elif current_state == 'event_location':
        event_location = message.text
        for_definite[-1]['location'] = event_location
        waiting_for_event_name_for_definite[user_id] = 'registration_deadline'
        await message.answer("Введите срок закрытия регистрации (в формате ГГГГ-ММ-ДД):")

    elif current_state == 'registration_deadline':
        registration_deadline = message.text
        for_definite[-1]['registration_deadline'] = registration_deadline
        waiting_for_event_name_for_definite[user_id] = 'input_max_participants'
        await message.answer("Пожалуйста, введите максимальное количество участников:")


    elif current_state == 'input_max_participants':

        try:

            max_participants = int(message.text)

            for_definite[-1]['max_participants'] = max_participants

            waiting_for_event_name_for_definite[user_id] = 'contact_info'  # Переходим к следующему состоянию

            await message.answer("Пожалуйста, введите вашу контактную информацию(Сайт где участники могут зарегистрироваться,ваш номер телефона или ваш юзер в телеграмме):")


        except ValueError:

            await message.answer("Пожалуйста, введите корректное число для максимального количества участников.")

    elif current_state == 'contact_info':

        contact_info = message.text

        for_definite[-1]['contact_info'] = contact_info  # Сохраняем контактную информацию

        # Добавление события в базу данных с ID пользователя

        add_event_to_db(for_definite[-1], user_id)
        delete_last_event(user_id)
        add_event_to_db_events_for_world(for_definite[-1], user_id)

        # Сохраняем мероприятие в словаре winners

        if user_id not in winners:
            winners[user_id] = {"мероприятия": []}

        winners[user_id]["мероприятия"].append({

            "название": for_definite[-1]['name'],

            "место": 1,  # Пример: устанавливаем место как 1 (можно изменить логику)

            "айдишка картинки": None  # Изначально нет изображения

        })

        # Подтверждение мероприятия

        confirmation_text = (f"Вы добавили мероприятие:\n"

                             f"Название: {for_definite[-1]['name']}\n"

                             f"Дата: {for_definite[-1]['date']}\n"

                             f"Время: {for_definite[-1]['time']}\n"

                             f"Место: {for_definite[-1]['location']}\n"

                             f"Срок регистрации: {for_definite[-1]['registration_deadline']}\n"

                             f"Максимальное количество участников: {for_definite[-1]['max_participants']}\n"

                             f"Тип мероприятия: {for_definite[-1]['type']}\n"

                             f"Контактная информация: {for_definite[-1]['contact_info']}\n"

                             f"Мероприятие успешно добавлено в систему!")

        waiting_for_event_name_for_definite.pop(user_id)  # Убираем пользователя из ожидания
        kb = types.ReplyKeyboardMarkup(
            keyboard=[

                [
                    types.KeyboardButton(text='Назад')
                ]
            ],
            resize_keyboard=True
        )
        await message.answer(confirmation_text,reply_markup=kb)
        print(get_all_events(user_id))#откладка
        print(get_all_events_events_for_world())

@dp.message(F.text == "Мои мероприятия")
async def list_events(message: types.Message):
    user_id = message.from_user.id
    events = get_all_events(user_id)  # Получаем мероприятия только для текущего пользователя

    if not events:
        await message.answer("Нет доступных мероприятий.")
        return

    public_events = []
    private_events = []

    # Разделяем мероприятия на две категории
    for event in events:
        if event[8] == 'Для общего пользования':  # Предполагаем, что тип мероприятия находится в 8-й колонке
            public_events.append(event)
        else:
            private_events.append(event)



    # Формируем и отправляем ответ
    await send_events_response(message, "Ваши мероприятия для общего пользования:", public_events)
    await send_events_response(message, "Ваши мероприятия для закрытого круга людей:", private_events)

async def send_events_response(message: types.Message, header: str, events: list):
    if events:
        response = f"{header}\n"
        inline_kb = [
            [types.InlineKeyboardButton(text=event[1], callback_data=f"event_{event[0]}")]
            for event in events
        ]
        response += "\n".join(f"- {event[1]}" for event in events)  # Добавляем названия мероприятий в текст

        # Создаем инлайн-клавиатуру из списка кнопок
        inline_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)
        await message.answer(response, reply_markup=inline_kb_markup)
    else:
        await message.answer(f"У вас нет мероприятий для {header.lower()}.")






@dp.callback_query(lambda c: c.data.startswith('event_'))
async def show_event_details(callback_query: types.CallbackQuery):
    event_id = callback_query.data.split('_')[1]  # Получаем ID мероприятия из callback_data
    user_id = callback_query.from_user.id
    events = get_all_events(user_id)  # Получаем мероприятия только для текущего пользователя

    # Ищем мероприятие по ID
    event = next((event for event in events if event[0] == int(event_id)), None)

    if event is None:
        await callback_query.answer("Мероприятие не найдено.")
        return

    event_info = (
        f"Название: {event[1]}\n"
        f"Дата: {event[2]}\n"
        f"Время: {event[3]}\n"
        f"Место: {event[4]}\n"
        f"Срок регистрации: {event[5]}\n"
        f"Максимальное количество участников: {event[6]}\n"

    )

    inline_kb = [
        [types.InlineKeyboardButton(text="Редактировать", callback_data=f"edit_event_{event_id}")],
        [types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_event_{event_id}")]
    ]

    inline_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)

    await callback_query.message.answer(event_info, reply_markup=inline_kb_markup)

@dp.callback_query(lambda c: c.data.startswith('edit_event_'))
async def edit_event(callback_query: types.CallbackQuery):
    global current_event_name  # Указываем, что используем глобальную переменную
    current_event_name = callback_query.data.split('_')[2]  # Получаем название мероприятия

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Ввести победителя', callback_data='enter_winner_for_word')],
        [types.InlineKeyboardButton(text='Ввести 2 места', callback_data='enter_second_place_for_word')],
        [types.InlineKeyboardButton(text='Ввести 3 места', callback_data='enter_third_place_for_word')],
        [types.InlineKeyboardButton(text='Добавить участников', callback_data='add_participants_for_word')],
        [types.InlineKeyboardButton(text='Назад', callback_data='back_to_menu_for_word')]
    ])
    await callback_query.message.answer("Выберите действие:", reply_markup=kb)
    await callback_query.answer()



@dp.callback_query(F.data == 'back_to_menu_for_word')
async def back_to_menu_for_word(callback: types.CallbackQuery):
    await cmd(callback.message)

@dp.callback_query(F.data == 'enter_winner_for_word')
async def _for_word(callback: types.CallbackQuery):
    global waiting_for_winner_id_for_word
    waiting_for_winner_id_for_word = True

    await callback.message.answer(
        f"Введите ID победителя:")
waiting_for_second_place_id=False
@dp.callback_query(F.data == 'enter_second_place_for_word')
async def _for_second_place(callback: types.CallbackQuery):
    global waiting_for_second_place_id
    waiting_for_second_place_id = True

    await callback.message.answer(
        "Введите ID второго места:"
    )

# Глобальная переменная для хранения ID второго места
second_place_id = None
waiting_for_third_place_id=False
@dp.callback_query(F.data == 'enter_third_place_for_word')
async def _for_third_place(callback: types.CallbackQuery):
    global waiting_for_third_place_id
    waiting_for_third_place_id = True

    await callback.message.answer(
        "Введите ID третьего места:"
    )
third_place_id = None
waiting_for_participant_id=False
@dp.callback_query(F.data == 'add_participants_for_word')
async def _for_participant(callback: types.CallbackQuery):
    global waiting_for_participant_id
    waiting_for_participant_id = True

    await callback.message.answer(
        "Введите ID участника:"
    )

# Глобальная переменная для хранения ID участника
participant_id = None

winner_images = {}  # Словарь для хранения изображений победителей по мероприятиям
current_event_id = None  # Переменная для хранения текущего ID мероприятия


# Глобальная переменная для хранения ID победителя
winner_id_for_word = None

waiting_for_image_for_sam = False

@dp.message(lambda message: waiting_for_winner_id_for_word)
async def winner_id_received_for_word(message: types.Message):
    global waiting_for_winner_id_for_word, winner_id_for_word
    winner_id_for_word = message.text
    winners1_for_word.append(winner_id_for_word)  # Добавляем ID победителя в список
    waiting_for_winner_id_for_word = False  # Сбрасываем флаг ожидания

    # Получаем последнее добавленное мероприятие
    last_event = winners[message.from_user.id]["мероприятия"][-1]

    # Сохраняем ID победителя в структуре данных winners
    if "победители" not in last_event:
        last_event["победители"] = []  # Создаем список победителей, если его нет
    last_event["победители"].append(winner_id_for_word)  # Добавляем ID победителя в мероприятие

    # Создаем клавиатуру с кнопками
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Выбрать изображение из готовых')
            ],
        ],
        resize_keyboard=True
    )

    await message.answer(f"ID победителя '{winner_id_for_word}' добавлен! \nПожалуйста, выберите действие:",
                         reply_markup=kb)


@dp.message(lambda message: message.text == 'Выбрать изображение из готовых')
async def choose_image_from_list(message: types.Message):
    # Проверяем, что список изображений не пуст
    if not lst_file_id_for1:
        await message.answer("Список изображений пуст.")
        return

    # Создаем клавиатуру с кнопками для выбора изображений
    inline_buttons = []

    # Добавляем кнопки для каждого изображения
    for index in range(len(lst_file_id_for1)):
        inline_buttons.append(
            [types.InlineKeyboardButton(text=f'Изображение {index + 1}', callback_data=f'image_{index}')])

    kb = types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    # Отправляем первое изображение с кнопкой
    await message.answer_photo(lst_file_id_for1[0], caption="Выберите изображение:", reply_markup=kb)

    # Если хотите отправить все изображения, можно использовать цикл
    for index in range(1, len(lst_file_id_for1)):
        await message.answer_photo(lst_file_id_for1[index], caption=f"Изображение {index + 1}", reply_markup=kb)


@dp.callback_query(lambda c: c.data.startswith('image_'))
async def process_image_selection(callback_query: types.CallbackQuery):
    global winner_id_for_word

    # Извлекаем индекс изображения
    image_index = int(callback_query.data.split('_')[1])
    print(f"Индекс выбранного изображения: {image_index}")  # Отладка

    try:
        selected_image_id = lst_file_id_for1[image_index]  # Сохраняю выбранное изображение
        print(f"Выбранное изображение ID: {selected_image_id}")

        last_event = winners[callback_query.from_user.id]["мероприятия"][-1]

        last_event["место"] = 1
        last_event["айдишка картинки"] = selected_image_id  #

        winner_data = {
            'winner_id': winner_id_for_word,
            'место': last_event["место"],
            'название': last_event["название"],
            'айдишка_картинки': selected_image_id,
            'user_id': callback_query.from_user.id
        }
        kb = types.ReplyKeyboardMarkup(
            keyboard=[

                [
                    types.KeyboardButton(text='Назад')
                ]
            ],
            resize_keyboard=True
        )
        # Добавляем победителя в базу данных
        add_winner_to_db(winner_data)

        # Ответ на нажатие кнопки
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               "Выбранное изображение сохранено в базе данных.",reply_markup=kb)
    except IndexError:
        await bot.answer_callback_query(callback_query.id, text="Ошибка: выбранное изображение не найдено.")
        print(f"Ошибка: индекс {image_index} вне диапазона для списка изображений.")  # Логируем ошибку
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, text="Произошла ошибка.")
        print(f"Произошла ошибка: {e}")

#вторые
@dp.message(lambda message: waiting_for_second_place_id)
async def second_place_id_received(message: types.Message):
    global waiting_for_second_place_id, second_place_id
    second_place_id = message.text
    winners2_for_word.append(second_place_id)  # Добавляем ID второго места в список
    waiting_for_second_place_id = False  # Сбрасываем флаг ожидания

    # Получаем последнее добавленное мероприятие
    last_event = winners[message.from_user.id]["мероприятия"][-1]

    # Сохраняем ID второго места в структуре данных winners
    if "вторые места" not in last_event:
        last_event["вторые места"] = []  # Создаем список вторых мест, если его нет
    last_event["вторые места"].append(second_place_id)  # Добавляем ID второго места в мероприятие

    # Создаем клавиатуру с кнопками
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Выбрать изображение для второго места')
            ],
        ],
        resize_keyboard=True
    )

    await message.answer(f"ID второго места '{second_place_id}' добавлен! \nПожалуйста, выберите действие:",
                         reply_markup=kb)

@dp.message(lambda message: message.text == 'Выбрать изображение для второго места')
async def choose_image_for_second_place(message: types.Message):
    # Проверяем, что список изображений не пуст
    if not lst_file_id_for2:
        await message.answer("Список изображений пуст.")
        return

    # Создаем клавиатуру с кнопками для выбора изображений
    inline_buttons = []

    # Добавляем кнопки для каждого изображения
    for index in range(len(lst_file_id_for2)):
        inline_buttons.append(
            [types.InlineKeyboardButton(text=f'Изображение {index + 1}', callback_data=f'second_image_{index}')])

    kb = types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    # Отправляем первое изображение с кнопкой
    await message.answer_photo(lst_file_id_for2[0], caption="Выберите изображение для второго места:", reply_markup=kb)

    # Если хотите отправить все изображения, можно использовать цикл
    for index in range(1, len(lst_file_id_for2)):
        await message.answer_photo(lst_file_id_for2[index], caption=f"Изображение {index + 1}", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith('second_image_'))
async def process_second_image_selection(callback_query: types.CallbackQuery):
    global second_place_id

    # Извлекаем индекс изображения
    image_index = int(callback_query.data.split('_')[2])
    print(f"Индекс выбранного изображения для второго места: {image_index}")  # Отладка

    try:
        selected_image_id = lst_file_id_for2[image_index]  # Сохраняю выбранное изображение
        print(f"Выбранное изображение ID для второго места: {selected_image_id}")

        last_event = winners[callback_query.from_user.id]["мероприятия"][-1]

        last_event["место"] = 2
        last_event["айдишка картинки"] = selected_image_id  #

        second_place_data = {
            'winner_id': second_place_id,
            'место': last_event["место"],
            'название': last_event["название"],
            'айдишка_картинки': selected_image_id,
            'user_id': callback_query.from_user.id
        }

        # Добавляем второе место в базу данных
        add_second_place_to_db(second_place_data)
        kb = types.ReplyKeyboardMarkup(
            keyboard=[

                [
                    types.KeyboardButton(text='Назад')
                ]
            ],
            resize_keyboard=True
        )
        # Ответ на нажатие кнопки
        await bot.answer_callback_query(callback_query.id)
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               "Выбранное изображение для второго места сохранено в базе данных.",reply_markup=kb)
    except IndexError:
        await bot.answer_callback_query(callback_query.id, text="Ошибка: выбранное изображение не найдено.")
        print(f"Ошибка: индекс {image_index} вне диапазона для списка изображений.")  # Логируем ошибку
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, text="Произошла ошибка.")
        print(f"Произошла ошибка: {e}")
@dp.message(lambda message: waiting_for_third_place_id)
async def third_place_id_received(message: types.Message):
    global waiting_for_third_place_id, third_place_id
    third_place_id = message.text
    winners3_for_word.append(third_place_id)  # Добавляем ID третьего места в список
    waiting_for_third_place_id = False  # Сбрасываем флаг ожидания

    # Получаем последнее добавленное мероприятие
    last_event = winners[message.from_user.id]["мероприятия"][-1]

    # Сохраняем ID третьего места в структуре данных winners
    if "третьи места" not in last_event:
        last_event["третьи места"] = []  # Создаем список третьих мест, если его нет
    last_event["третьи места"].append(third_place_id)  # Добавляем ID третьего места в мероприятие

    # Создаем клавиатуру с кнопками
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Выбрать изображение для третьего места')
            ],
        ],
        resize_keyboard=True
    )

    await message.answer(f"ID третьего места '{third_place_id}' добавлен! \nПожалуйста, выберите действие:",
                         reply_markup=kb)

@dp.message(lambda message: message.text == 'Выбрать изображение для третьего места')
async def choose_image_for_third_place(message: types.Message):
    # Проверяем, что список изображений не пуст
    if not lst_file_id_for3:
        await message.answer("Список изображений пуст.")
        return

    # Создаем клавиатуру с кнопками для выбора изображений
    inline_buttons = []

    # Добавляем кнопки для каждого изображения
    for index in range(len(lst_file_id_for3)):
        inline_buttons.append(
            [types.InlineKeyboardButton(text=f'Изображение {index + 1}', callback_data=f'third_image_{index}')])

    kb = types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    # Отправляем первое изображение с кнопкой
    await message.answer_photo(lst_file_id_for3[0], caption="Выберите изображение для третьего места:", reply_markup=kb)

    # Если хотите отправить все изображения, можно использовать цикл
    for index in range(1, len(lst_file_id_for3)):
        await message.answer_photo(lst_file_id_for3[index], caption=f"Изображение {index + 1}", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith('third_image_'))
async def process_third_image_selection(callback_query: types.CallbackQuery):
    global third_place_id
    kb = types.ReplyKeyboardMarkup(
        keyboard=[

            [
                types.KeyboardButton(text='Назад')
            ]
        ],
        resize_keyboard=True
    )
    # Извлекаем индекс изображения
    image_index = int(callback_query.data.split('_')[2])
    print(f"Индекс выбранного изображения для третьего места: {image_index}")  # Отладка

    try:
        selected_image_id = lst_file_id_for3[image_index]  # Сохраняю выбранное изображение
        print(f"Выбранное изображение ID для третьего места: {selected_image_id}")

        last_event = winners[callback_query.from_user.id]["мероприятия"][-1]

        last_event["место"] = 3
        last_event["айдишка картинки"] = selected_image_id  #

        third_place_data = {
            'winner_id': third_place_id,
            'место': last_event["место"],
            'название': last_event["название"],
            'айдишка_картинки': selected_image_id,
            'user_id': callback_query.from_user.id
        }

        # Добавляем третье место в базу данных
        add_third_place_to_db(third_place_data)
        await bot.answer_callback_query(callback_query.id)
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               "Выбранное изображение для третьего места сохранено в базе данных.",reply_markup=kb)
    except IndexError:
        await bot.answer_callback_query(callback_query.id, text="Ошибка: выбранное изображение не найдено.")
        print(f"Ошибка: индекс {image_index} вне диапазона для списка изображений.")  # Логируем ошибку
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, text="Произошла ошибка.")
        print(f"Произошла ошибка: {e}")

#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
@dp.message(lambda message: waiting_for_participant_id)
async def participant_id_received(message: types.Message):
    global waiting_for_participant_id, participant_id
    participant_id = message.text
    participants_for_word.append(participant_id)  # Добавляем ID третьего места в список
    waiting_for_participant_id = False  # Сбрасываем флаг ожидания

    # Получаем последнее добавленное мероприятие
    last_event = winners[message.from_user.id]["мероприятия"][-1]

    # Сохраняем ID третьего места в структуре данных winners
    if "участники" not in last_event:
        last_event["участники"] = []  # Создаем список третьих мест, если его нет
    last_event["участники"].append(participant_id)  # Добавляем ID третьего места в мероприятие

    # Создаем клавиатуру с кнопками
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Выбрать изображение для участников')
            ],
        ],
        resize_keyboard=True
    )

    await message.answer(f"ID участника '{participant_id}' добавлен! \nПожалуйста, выберите действие:",
                         reply_markup=kb)

@dp.message(lambda message: message.text == 'Выбрать изображение для участников')
async def choose_image_for_participant(message: types.Message):
    # Проверяем, что список изображений не пуст
    if not lst_file_id_for_participants:
        await message.answer("Список изображений пуст.")
        return

    # Создаем клавиатуру с кнопками для выбора изображений
    inline_buttons = []

    # Добавляем кнопки для каждого изображения
    for index in range(len(lst_file_id_for_participants)):
        inline_buttons.append(
            [types.InlineKeyboardButton(text=f'Изображение {index + 1}', callback_data=f'participants_image_{index}')])

    kb = types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    # Отправляем первое изображение с кнопкой
    await message.answer_photo(lst_file_id_for_participants[0], caption="Выберите изображение для участника:", reply_markup=kb)

    # Если хотите отправить все изображения, можно использовать цикл
    for index in range(1, len(lst_file_id_for_participants)):
        await message.answer_photo(lst_file_id_for_participants[index], caption=f"Изображение {index + 1}", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith('participants_image_'))
async def process_participant_image_selection(callback_query: types.CallbackQuery):
    global participant_id
    kb = types.ReplyKeyboardMarkup(
        keyboard=[

            [
                types.KeyboardButton(text='Назад')
            ]
        ],
        resize_keyboard=True
    )
    # Извлекаем индекс изображения
    image_index = int(callback_query.data.split('_')[2])
    print(f"Индекс выбранного изображения для участника: {image_index}")  # Отладка

    try:
        selected_image_id = lst_file_id_for_participants[image_index]  # Сохраняю выбранное изображение
        print(f"Выбранное изображение ID для участника: {selected_image_id}")

        last_event = winners[callback_query.from_user.id]["мероприятия"][-1]

        last_event["место"] = "Участник"
        last_event["айдишка картинки"] = selected_image_id  #

        participant_place_data = {
            'winner_id': participant_id,
            'место': last_event["место"],
            'название': last_event["название"],
            'айдишка_картинки': selected_image_id,
            'user_id': callback_query.from_user.id
        }

        # Добавляем третье место в базу данных
        add_participant_to_db(participant_place_data)
        await bot.answer_callback_query(callback_query.id)
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               "Выбранное изображение для третьего места сохранено в базе данных.",reply_markup=kb)
    except IndexError:
        await bot.answer_callback_query(callback_query.id, text="Ошибка: выбранное изображение не найдено.")
        print(f"Ошибка: индекс {image_index} вне диапазона для списка изображений.")  # Логируем ошибку
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, text="Произошла ошибка.")
        print(f"Произошла ошибка: {e}")
#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

@dp.message(lambda message: waiting_for_participant_id)
async def participant_id_received(message: types.Message):
    global waiting_for_participant_id, participant_id
    participant_id = message.text
    participants_for_word.append(participant_id)  # Добавляем ID участника в список
    waiting_for_participant_id = False  # Сбрасываем флаг ожидания

    # Создаем клавиатуру с кнопками
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Выбрать изображение для участника')
            ],
        ],
        resize_keyboard=True
    )

    await message.answer(f"ID участника '{participant_id}' добавлен! \nПожалуйста, выберите действие:",
                         reply_markup=kb)

@dp.message(lambda message: message.text == 'Выбрать изображение для участника')
async def choose_image_for_participant(message: types.Message):
    # Проверяем, что список изображений не пуст
    if not lst_file_id_for_participants:
        await message.answer("Список изображений пуст.")
        return

    # Создаем клавиатуру с кнопками для выбора изображений
    inline_buttons = []

    # Добавляем кнопки для каждого изображения
    for index in range(len(lst_file_id_for_participants)):
        inline_buttons.append(
            [types.InlineKeyboardButton(text=f'Изображение {index + 1}', callback_data=f'participant_image_{index}')])

    kb = types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    # Отправляем первое изображение с кнопкой
    await message.answer_photo(lst_file_id_for_participants[0], caption="Выберите изображение для участника:", reply_markup=kb)

    # Если хотите отправить все изображения, можно использовать цикл
    for index in range(1, len(lst_file_id_for_participants)):
        await message.answer_photo(lst_file_id_for_participants[index], caption=f"Изображение {index + 1}", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith('participant_image_'))
async def process_participant_image_selection(callback_query: types.CallbackQuery):
    global participant_id

    # Извлекаем индекс изображения
    image_index = int(callback_query.data.split('_')[2])
    print(f"Индекс выбранного изображения для участника: {image_index}")  # Отладка

    try:
        selected_image_id = lst_file_id_for_participants[image_index]  # Сохраняю выбранное изображение
        print(f"Выбранное изображение ID для участника: {selected_image_id}")

        last_event = winners[callback_query.from_user.id]["мероприятия"][-1]

        last_event["место"] = 3
        last_event["айдишка картинки"] = selected_image_id  #

        participant_data = {
            'winner_id': third_place_id,
            'место': last_event["место"],
            'название': last_event["название"],
            'айдишка_картинки': selected_image_id,
            'user_id': callback_query.from_user.id
        }

        kb = types.ReplyKeyboardMarkup(
            keyboard=[

                [
                    types.KeyboardButton(text='Назад')
                ]
            ],
            resize_keyboard=True
        )
        # Добавляем участника в базу данных
        add_participant_to_db(participant_data)

        # Ответ на нажатие кнопки
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               "Выбранное изображение для участника сохранено в базе данных.",reply_markup=kb)
    except IndexError:
        await bot.answer_callback_query(callback_query.id, text="Ошибка: выбранное изображение не найдено.")
        print(f"Ошибка: индекс {image_index} вне диапазона для списка изображений.")  # Логируем ошибку
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, text="Произошла ошибка.")
        print(f"Произошла ошибка: {e}")

@dp.callback_query(lambda c: c.data.startswith('delete_event_'))
async def delete_event(callback_query: types.CallbackQuery):
    event_id = callback_query.data.split('_')[2]  # Получаем ID мероприятия из callback_data
    user_id = callback_query.from_user.id

    # Логика удаления мероприятия из базы данных
    delete_event_from_db(event_id, user_id)  # Предположим, у вас есть такая функция для удаления мероприятия

    await callback_query.answer("Мероприятие успешно удалено.")
    await callback_query.message.answer("Вы можете посмотреть свои мероприятия снова.")

# Функция для обновления названия мероприятия в базе данных
def update_event_name_in_db(user_id, event_id, new_event_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Events
        SET event_name = ?
        WHERE event_id = ? AND user_id = ?
    ''', (new_event_name, event_id, user_id))
    conn.commit()
    conn.close()

# Функция для удаления мероприятия из базы данных
def delete_event_from_db(event_id, user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Events WHERE event_id = ? AND user_id = ?', (event_id, user_id))
    conn.commit()
    conn.close()


@dp.message(F.text == "Новые мероприятия")
async def new_events(message: types.Message):
    events = get_all_events_events_for_world()  # Получаем все мероприятия из базы данных
    print("Все мероприятия:", events)  # Выводим все мероприятия для отладки

    if not events:
        await message.answer("Нет новых мероприятий для общего пользования.")
        return

    public_events = []

    # Фильтруем мероприятия для общего пользования
    for event in events:
        print("Тип мероприятия:", event[8])  # Выводим тип мероприятия для отладки
        if event[8] == 'Для общего пользования':  # Предполагаем, что тип мероприятия находится в 7-й колонке
            public_events.append(event)

    if public_events:
        response = "Мероприятия в котщрых можно поучастовавать:\n"
        inline_kb = []
        for event in public_events:
            response += f"- {event[1]}\n"  # Добавляем название мероприятия в текст
            inline_kb.append([types.InlineKeyboardButton(text=event[1],
                                                         callback_data=f"event_{event[0]}")])  # Добавляем кнопку с названием мероприятия

        # Создаем инлайн-клавиатуру из списка кнопок
        inline_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)
        await message.answer(response, reply_markup=inline_kb_markup)
    else:
        await message.answer("Нет новых мероприятий для общего пользования.")

@dp.message(F.text == 'Мои достижения')
async def send_achievements(message: types.Message):
    user_id = message.from_user.id
    achievements = get_all_winners(user_id)

    print(f"Полученные достижения для user_id {user_id}: {achievements}")  # Логирование

    if not achievements:
        await message.answer("У вас нет достижений.")
        return

    # Формируем ответ
    response_text = "Ваши достижения:\n\n"
    for achievement in achievements:
        try:
            winner_id, place, event_name, image_id = achievement  # Ожидаем 4 значения
            response_text += f"Мероприятие: {event_name}\nМесто: {place}\n\n"

            # Отправляем изображение
            await bot.send_photo(chat_id=user_id, photo=image_id, caption=response_text)
        except ValueError as e:
            print(f"Ошибка распаковки: {e}")  # Логируем ошибку
            await message.answer("Ошибка при обработке ваших достижений.")

    await message.answer("Все ваши достижения отправлены! 🎉")




@dp.message(F.text == "Назад")
async def back_to_main_menu(message: types.Message):
    await cmd(message)  # Возвращаемся в главное меню
waiting_for_question = False
user_id = None
user_question = None
SUPPORT_USER_ID=5123017159
@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    global waiting_for_question, user_id
    waiting_for_question = True
    user_id = message.from_user.id  # Сохраняем ID пользователя
    await message.answer("Напишите здесь ваш вопрос, и мы на него ответим.")

@dp.message(lambda message: waiting_for_question)
async def receive_question(message: types.Message):
    global waiting_for_question, user_id, user_question
    user_question = message.text  # Сохраняем текст вопроса
    await bot.send_message(SUPPORT_USER_ID, f"Вопрос от пользователя {user_id}: {user_question}\nНапишите ответ:")
    await bot.send_message(user_id, "Ваш вопрос принят. Мы ответим на него в ближайшее время.")
    waiting_for_question = False  # Сбрасываем состояние

@dp.message(lambda message: message.from_user.id == SUPPORT_USER_ID)
async def send_answer(message: types.Message):
    global user_id, user_question
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='Мои достижения'), types.KeyboardButton(text='Новые мероприятия')],
            [types.KeyboardButton(text='Мои мероприятия'), types.KeyboardButton(text='Создать мероприятие')]
        ],
        resize_keyboard=True
    )
    if user_id and user_question:  # Проверяем, есть ли предыдущий вопрос
        await bot.send_message(user_id, f"Ваш вопрос: {user_question}\nОтвет: {message.text}\n\nЧтобы задать еще вопросы снова нажмите на /help или выберете действие:",reply_markup=kb)
        await bot.send_message(SUPPORT_USER_ID, "Ответ отправлен пользователю.")  # Подтверждение отправки
        user_id = None  # Сбрасываем ID пользователя
        user_question = None  # Сбрасываем текст вопроса







async def main():
    await on_startup()
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(5)  # Ждем перед повторной попыткой

if __name__ == '__main__':
    asyncio.run(main())


