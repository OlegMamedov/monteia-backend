import bcrypt
from fastapi import HTTPException
import random
import json
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.responses import FileResponse
import requests
from config import PRIVATE_KEY, PUBLIC_KEY, ALGORITHM, GREEN_SMS_PASSWORD, GREEN_SMS_USER
from starlette.background import BackgroundTasks
from gtts import gTTS
from greensms.client import GreenSMS
import uuid
import os
import hashlib
from config import AUTH_GIGACHAT


#Синтез текста в голос
def remove_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Error removing file: {e}")

def text_in_audio(text: str):

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join("static/audio", filename)

    # Создание аудио из текста
    tts = gTTS(text, lang='ru')
    tts.save(filepath)

    return FileResponse(path=filepath, filename=filename, media_type='audio/mpeg')




#Генерация ответа GIGACHAT
def get_access_token_from_gigachat():
    url = "https://developers.sber.ru/docs/api/gigachat/auth/v2/oauth"

    payload={
    "scope": "GIGACHAT_API_PERS"
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    "Authorization": f"Basic {AUTH_GIGACHAT}",
    "RqUID": str(uuid.uuid4())
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    ACCESS_TOKEN_GIGA = response.json().get("access_token")

    return ACCESS_TOKEN_GIGA

def get_response_from_gigachat(query: str, cards: list):

    ACCESS_TOKEN_GIGA = get_access_token_from_gigachat()
    crd = json.dumps(cards).replace("[", "").replace("]", "").replace('"', "")
    example = '{"cards": [{"id": "шут", "text": предсказание по карте}], "sum": итог}'
    message = f'''Представь что ты гадалка. Объясни значение каждой карты в контексте моего запроса кратко, в конце подведи кратко итоги всего расклада
                 Запрос: {query}
                 Выпавшие карты: {crd}

                 Ответ дай в формате json по примеру: {example}'''

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

    data_bot = json.loads(bot_message)

    return data_bot


def create_signature(secret_key, request_data):
    # Create the signature by concatenating the secret key and the JSON data
    signature_data = f"{secret_key}{json.dumps(request_data)}"
    # Calculate the MD5 hash of the signature data
    signature = hashlib.md5(signature_data.encode()).hexdigest()
    return signature

def send_request(api_url, merchant_id, request_data, secret_key):
    # Create the signature
    signature = create_signature(secret_key, request_data)
    # Prepare the request data
    data = {
        "merchant_id": merchant_id,
        "signature": signature,
        **request_data
    }
    # Send the POST request
    response = requests.post(api_url, json=data)
    return response

# Генерация рандомного id карты
def generate_random_card():
    return random.randint(1, 78)

# Генерация 6 значного кода
def generate_verify_code(length=6):
    return ''.join(random.choices('0123456789', k=length))

# Отправка кода по номеру
def send_verify_code(phone_number, code):
    message = f'Ваш код подтверждения: {code}. Никому его не показывайте.'
    client = GreenSMS(user=GREEN_SMS_USER, password=GREEN_SMS_PASSWORD)
    client.sms.send(to=phone_number, txt=message)

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
        print(f"JWTError: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


# Хеширование пароля
def generate_password_hash(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
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