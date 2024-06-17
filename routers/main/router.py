import datetime
import random
import json

from datetime import timedelta, datetime
from starlette.background import BackgroundTasks

from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from database.models import User, Token, Journals, Cards
from routers.main.schemas import RegisterSchema, LoginSchema, AuthSchema
from database.utils import get_user_by_login, get_user_by_id_and_number, count_entry_by_user_id, delete_journal_by_entry_number, get_journal_by_entry_number_and_userid, get_card_by_id, get_div_by_name
from database.db import async_session
from routers.main.utils import generate_password_hash, get_zodiac_sign, create_access_token, decode_token, generate_verify_code, send_verify_code, check_password, lucky_num, text_in_audio, get_response_from_gigachat


router = APIRouter(prefix = "", tags=["Main"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/")


@router.get('/user/me')
async def get_user(token: str = Depends(oauth2_scheme)):

    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        username = payload.get("username")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_number(id, username)

    if not user:
        return JSONResponse({'error': 'User not found'}, 404)

    current_time = datetime.utcnow()

    if current_time - user.lucky_rait_time >= timedelta(hours=24):
        user.lucky_rait = lucky_num()
        user.lucky_rait_time = current_time
        async with async_session() as session:
            await session.commit()


    return {
        'first_name': user.f_name,
        'last_name': user.l_name,
        'bithday_date': user.birthday_date,
        'zodiac_sign': user.zodiac_sign,
        'lucky_raiting': user.lucky_rait
    }



@router.post('/register/')
async def verificate_user(data: RegisterSchema):
    user = await get_user_by_login(data.number)

    if user:
        return JSONResponse({'error': 'Phone number already exists.'}, 401)


    user = User(number=data.number,
                password_hash=generate_password_hash(data.password),
                f_name=data.f_name,
                l_name=data.l_name,
                birthday_date = data.birthday_date,
                lucky_rait_time = datetime.utcnow(),
                lucky_rait = lucky_num(),
                created_at = datetime.utcnow(),
                zodiac_sign = get_zodiac_sign(str(data.birthday_date)))


    try:
        async with async_session() as session:
            session.add(user)
            await session.commit()
        return {'message': 'User registered successfully'}
    except Exception as e:
        return JSONResponse({'error': str(e)}, 500)



@router.post('/login/')
async def verificate_number(data: LoginSchema):
    user = await get_user_by_login(data.number)

    if user:
        return JSONResponse({'error': 'You are ready in system'},401)

    code = generate_verify_code()

    sms_sent = send_verify_code(data.number, code)
    if sms_sent:
        return JSONResponse({'message': 'Check code in your phone'})
    else:
        return JSONResponse({'error': 'Check your phone number'},401)




@router.post('/auth/')
async def auth(data: AuthSchema):
    user = await get_user_by_login(data.number)

    if user and user.code == data.code:

        token = create_access_token(data={"sub": user.l_name,
                                          "user_id": user.id,
                                          "username": user.username})

        new_token = Token(token = token,
                          user_id = user.id)

        async with async_session() as session:
            session.add(new_token)
            await session.commit()

        return {"access_token": token,
                "token_type": "Bearer"}


    return JSONResponse({'error': 'Not found'}, 404)


@router.post("/journal/add/entry")
async def add_entry(text_for_entry: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        username = payload.get("username")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_number(id, username)

    nums_entry = await count_entry_by_user_id(user.id)

    entry = Journals(user_id=user.id,
                     entry_number=nums_entry + 1,
                     content = text_for_entry)

    async with async_session() as session:
        session.add(entry)
        await session.commit()

    return JSONResponse({'message': 'The entry was successfully added'}, 200)


@router.get("/journal/get/entry")
async def get_journal(entry_number: int, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        username = payload.get("username")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_number(id, username)

    if not user:
        return JSONResponse({'error': 'User not found'}, 404)

    journal = await get_journal_by_entry_number_and_userid(entry_number, user.id)

    return {"entry_number": journal.entry_number,
            "content": journal.content}

@router.delete("/journal/delete/entry")
async def del_entry(entry_number: int, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        username = payload.get("username")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_number(id, username)

    if not user:
        return JSONResponse({'error': 'User not found'}, 404)


    journal = await get_journal_by_entry_number_and_userid(entry_number, user.id)

    if not journal:
        return JSONResponse({'error': 'User not found'}, 404)

    await delete_journal_by_entry_number(entry_number, user.id)

    return JSONResponse({'message': 'Entry was deleted success'}, 201)

@router.post("/journal/edit/entry")
async def edit_entry(entry_number: int, content: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    try:
        id = payload.get("user_id")
        username = payload.get("username")
    except:
        JSONResponse({'error': 'You don\'t authenticated'})


    user = await get_user_by_id_and_number(id, username)

    get_entry = await get_journal_by_entry_number_and_userid(entry_number, user.id)

    get_entry.content = content

    async with async_session() as session:
        session.add(get_entry)
        await session.commit()

    return JSONResponse({'message': 'Entry was edited'}, 201)


@router.post("/chat/")
async def chat(query: str):
    div = get_div_by_name(query)

    randomId_cards = []
    randomName_card = []
    while len(randomId_cards) < div.id:
        randomId_cards.append(random.randint(1, 78))

    for i in randomId_cards:
        card = await get_card_by_id(i)
        randomName_card.append(card.name)
    try:
        chat_response = get_response_from_gigachat(query, randomName_card)
        audio_response = []
        for i in chat_response["cards"]:
            audio_response.append(text_in_audio(i["text"]))

        audio_response.append(chat_response["sum"])
        return audio_response

    except:
        JSONResponse({'error': 'bot was not responses'}, 401)





