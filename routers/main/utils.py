import bcrypt
from fastapi import HTTPException
import random
from jose import JWTError, jwt
from datetime import datetime, timedelta
import requests
import torch
from config import PRIVATE_KEY, PUBLIC_KEY, ALGORITHM, SMSRU_API_ID, ACCESS_TOKEN_GIGA, API_KEY_LOVO



#Синтез текста в голос
def create_query():
    url = "https://api.ttsmaker.com/v1/get-voice-list"

    headers = {
        'token': 'ttsmaker_demo_token',
        'language': 'ru'
    }

    return requests.get(url, headers=headers)

def create_tts(text: str):
    url = "https://api.genny.lovo.ai/api/v1/tts"

    payload = {
        "speaker": "63b409eb241a82001d51c782",
        "text": text,
        "speed": 1
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": API_KEY_LOVO
    }

    return requests.post(url, json=payload, headers=headers).json()

    

def text_in_audio(job_id: str):
    pass

#Генерация ответа GIGACHAT
def get_response_from_gigachat():
    message = '''Представь что ты гадалка. Объясни значение каждой карты в контексте моего запроса кратко, в конце подвети кратко итоги всего расклада
                 Запрос: Расклад на неделю
                 Выпавшие карты: шут, справедливость, паж кубов

                 Ответ дай в формате json, пример: {"cards": [{"id": "шут", "text": предсказание по карте}], "sum": итог}'''

    url = "https://developers.sber.ru/docs/api/gigachat/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN_GIGA}'
    }

    payload = {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 1.0,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1
    }

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()

    bot_message = response_data['choices'][0]['message']['content']

    return bot_message

# Генерация 6 значного кода
def generate_verify_code(length=6):
    return ''.join(random.choices('0123456789', k=length))

# Отправка кода по номеру
def send_verify_code(phone_number, code):
    url = 'https://sms.ru/sms/send'
    payload = {
        'api_id': SMSRU_API_ID,
        'to': phone_number,
        'msg': f"Ваш код подтверждения: {code}",
        'json': 1
    }

    response = requests.get(url, params=payload)
    return response.json()

# Генерация числа удачи
def lucky_num():
    return random.randint(5, 10)

# Создание токена
def create_access_token(data: dict):
    to_encode = data.copy()  
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Расшифровка токена
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError as e:
        print(f"JWTError: {e}")  # Добавьте отладочное сообщение
        raise HTTPException(status_code=401, detail="Invalid credentials")


# Хеширование пароля
def generate_password_hash(password: str):
    salt = bcrypt.gensalt()
    # Хеширование пароля с использованием соли
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Возвращаем хешированный пароль в виде строки
    return hashed_password.decode('utf-8')

# Проверка хеша пароля
def check_password(password: str, hashed_password: str):

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Определение знака зодиака по дате рождения
def get_zodiac_sign(birthday_date):
    birthday_date = datetime.strptime(birthday_date, "%Y-%m-%d")
    day = birthday_date.day
    month = birthday_date.month
    zodiac_signs = {
        (1, 20): "Козерог",
        (2, 19): "Водолей",
        (3, 21): "Овен",
        (4, 20): "Телец",
        (5, 21): "Близнецы",
        (6, 21): "Рак",
        (7, 23): "Лев",
        (8, 23): "Дева",
        (9, 23): "Весы",
        (10, 23): "Скорпион",
        (11, 22): "Стрелец",
        (12, 22): "Козерог"
    }
    for sign_date, sign_name in sorted(zodiac_signs.items(), reverse=True):
        if (month, day) >= sign_date:
            return sign_name
    return "Invalid Date"